import os

import pytest

from app import create_app, db
from app.models import Role, User


@pytest.fixture()
def app(tmp_path):
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(tmp_path / 'test.sqlite')
    app.config['UPLOAD_FOLDER'] = str(tmp_path / 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SERVER_NAME'] = 'localhost'

    with app.app_context():
        db.create_all()
        Role.insert_roles()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def admin(app):
    role = Role.query.filter_by(name='Administrator').first()
    user = User(username='admin', email='admin@example.com', name='Admin',
                role=role, confirmed=True)
    user.set_password('secret123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def admin_client(client, admin):
    client.post('/auth/login', data={'username': 'admin', 'password': 'secret123'},
                follow_redirects=True)
    return client
