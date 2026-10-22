import os
from datetime import datetime

from flask import Flask

from config import config

from .extensions import csrf, db, login_manager, mail, migrate


def _stamp_migrations():
    """Mark the database as up to date so `flask db upgrade` stays consistent.

    Flask runs CLI commands inside an application context, so the current
    database is picked up automatically.
    """
    try:
        from flask_migrate import stamp

        stamp()
    except Exception as exc:  # pragma: no cover - migrations are optional locally
        print('Could not stamp migrations: %s' % exc)


def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)
    config_name = config_name or os.environ.get('FLASK_CONFIG', 'default')

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    os.makedirs(app.instance_path, exist_ok=True)

    login_manager.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .api import api as api_blueprint
    from .admin import admin as admin_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .models import AnonymousUser, LegalPage, Permission, Role, SiteSetting, User

    login_manager.anonymous_user = AnonymousUser

    @app.context_processor
    def inject_site_settings():
        """Expose editable site wide settings to every template."""
        from .main.forms import NewsletterForm

        try:
            settings = SiteSetting.as_dict()
        except Exception:  # pragma: no cover - database not ready yet
            settings = []
        try:
            legal_pages = LegalPage.query.order_by(LegalPage.title).all()
        except Exception:  # pragma: no cover - database not ready yet
            legal_pages = []
        return dict(site_settings=settings,
                    legal_pages=legal_pages,
                    newsletter_form=NewsletterForm(),
                    site_url=app.config['SITE_URL'].rstrip('/'),
                    api_base=app.config['API_BASE'].rstrip('/'),
                    current_year=datetime.now().year,
                    payments_enabled=bool(app.config.get('FLW_SECRET_KEY')),
                    payment_currency=app.config['PAYMENT_CURRENCY'],
                    deposit_percent=app.config['PAYMENT_DEPOSIT_PERCENT'])

    @app.cli.command('init-db')
    def init_db():
        """Create the tables and load the starter content."""
        from .seed import seed_all

        db.create_all()
        Role.insert_roles()
        seed_all()
        db.session.commit()
        _stamp_migrations()
        print('Database initialised.')

    @app.cli.command('create-admin')
    def create_admin():
        """Create an administrator account (username, email, password)."""
        import getpass
        import sys

        username = input('Username: ').strip()
        email = input('Email: ').strip()
        password = getpass.getpass('Password: ')
        if not username or not email or not password:
            print('Username, email and password are required.')
            sys.exit(1)

        if User.query.filter((User.username == username) | (User.email == email)).first():
            print('That user already exists.')
            sys.exit(1)

        role = Role.query.filter_by(name='Administrator').first()
        if role is None:
            Role.insert_roles()
            role = Role.query.filter_by(name='Administrator').first()

        user = User(username=username, email=email, name=username, role=role, confirmed=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print('Administrator %s created.' % username)

    @app.context_processor
    def inject_permissions():
        return dict(Permission=Permission)

    return app
