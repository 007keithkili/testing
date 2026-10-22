import re
from datetime import datetime, timezone

from flask import current_app
from flask_login import UserMixin
from sqlalchemy import event
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db, login_manager


def utcnow():
    return datetime.now(timezone.utc)


def slugify(value):
    """Turn a human readable title into a URL friendly slug."""
    value = re.sub(r'[^\w\s-]', '', str(value)).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


def _auto_slug(mapper, connection, target):
    """Fill in a slug from the title when it was left empty."""
    if getattr(target, 'slug', None):
        return
    title = getattr(target, 'name', None) or getattr(target, 'title', None) or ''
    target.slug = slugify(title)


class Permission:
    """Bit flags describing what a role is allowed to do."""

    ADMIN = 0x01
    EDIT_CONTENT = 0x02
    VIEW_INQUIRIES = 0x04

    @staticmethod
    def names():
        return ['ADMIN', 'EDIT_CONTENT', 'VIEW_INQUIRIES']


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer, default=0)

    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': Permission.VIEW_INQUIRIES,
            'Editor': Permission.VIEW_INQUIRIES | Permission.EDIT_CONTENT,
            'Administrator': Permission.ADMIN | Permission.EDIT_CONTENT | Permission.VIEW_INQUIRIES,
        }
        for name, permissions in roles.items():
            role = Role.query.filter_by(name=name).first()
            if role is None:
                role = Role(name=name)
            role.reset_permissions()
            role.permissions = permissions
            db.session.add(role)
        db.session.commit()

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, permission):
        return (self.permissions & permission) == permission

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utcnow)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.can(Permission.ADMIN)

    def can(self, permission):
        if self.is_authenticated and self.role:
            return self.role.has_permission(permission)
        return False

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser:
    """Stand-in for a visitor that is not signed in."""

    is_authenticated = False
    is_active = False
    is_anonymous = True

    def can(self, permission):
        return False

    def __repr__(self):
        return '<AnonymousUser>'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class SiteSetting(db.Model):
    """Simple key/value store for editable site wide content."""

    __tablename__ = 'site_settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False, index=True)
    value = db.Column(db.Text)

    @staticmethod
    def get(key, default=''):
        setting = SiteSetting.query.filter_by(key=key).first()
        return setting.value if setting and setting.value is not None else default

    @staticmethod
    def set(key, value):
        setting = SiteSetting.query.filter_by(key=key).first()
        if setting is None:
            setting = SiteSetting(key=key)
        setting.value = value
        db.session.add(setting)
        return setting

    @staticmethod
    def as_dict():
        return {s.key: s.value for s in SiteSetting.query.all()}

    def __repr__(self):
        return '<SiteSetting %r>' % self.key


class Destination(db.Model):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(160), unique=True, nullable=False, index=True)
    tag = db.Column(db.String(64), default='Safari')
    image_url = db.Column(db.String(512))
    description = db.Column(db.Text)
    highlights = db.Column(db.JSON, default=list)
    price = db.Column(db.String(64))
    price_value = db.Column(db.Integer, default=0)
    duration_days = db.Column(db.Integer, default=1)
    location = db.Column(db.String(128))
    is_featured = db.Column(db.Boolean, default=False, index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utcnow)

    @property
    def duration(self):
        return '%d Days' % self.duration_days

    @property
    def price_display(self):
        return self.price or ('$%s' % self.price_value)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'tag': self.tag,
            'image_url': self.image_url,
            'description': self.description,
            'price': self.price_display,
            'duration': self.duration,
            'location': self.location,
            'url': '/destinations/' + self.slug,
        }

    def __repr__(self):
        return '<Destination %r>' % self.name


class Package(db.Model):
    __tablename__ = 'packages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(160), unique=True, nullable=False, index=True)
    tagline = db.Column(db.String(255))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(512))
    price = db.Column(db.String(64))
    price_value = db.Column(db.Integer, default=0)
    days = db.Column(db.Integer, default=1)
    nights = db.Column(db.Integer, default=0)
    features = db.Column(db.JSON, default=list)
    tags = db.Column(db.JSON, default=list)
    comparison = db.Column(db.JSON, default=dict)
    highlight = db.Column(db.String(64))
    is_featured = db.Column(db.Boolean, default=False, index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utcnow)

    @property
    def duration(self):
        return '%d Days / %d Nights' % (self.days, self.nights)

    @property
    def price_display(self):
        return self.price or ('$%s' % self.price_value)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'tagline': self.tagline,
            'price': self.price_display,
            'duration': self.duration,
            'features': self.features or [],
            'tags': self.tags or [],
            'url': '/packages/' + self.slug,
        }

    def __repr__(self):
        return '<Package %r>' % self.name


class Experience(db.Model):
    """Additional experiences listed under the packages page."""

    __tablename__ = 'experiences'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    duration = db.Column(db.String(64))
    highlights = db.Column(db.Text)
    price = db.Column(db.String(64))
    image_url = db.Column(db.String(512))
    is_active = db.Column(db.Boolean, default=True, index=True)
    sort_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Experience %r>' % self.title


class Wildlife(db.Model):
    __tablename__ = 'wildlife'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    tag = db.Column(db.String(64))
    image_url = db.Column(db.String(512))
    sort_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Wildlife %r>' % self.name


class Service(db.Model):
    """Other services grid on the home page."""

    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(64))
    sort_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Service %r>' % self.title


class Feature(db.Model):
    """Why choose us cards on the about page."""

    __tablename__ = 'features'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(64))
    sort_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Feature %r>' % self.title


class Touchpoint(db.Model):
    """Physical touchpoint cards on the about page."""

    __tablename__ = 'touchpoints'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    bullets = db.Column(db.JSON, default=list)
    image_url = db.Column(db.String(512))
    sort_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Touchpoint %r>' % self.title


class Testimonial(db.Model):
    __tablename__ = 'testimonials'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(128), nullable=False)
    trip = db.Column(db.String(128))
    quote = db.Column(db.Text)
    image_url = db.Column(db.String(512))
    sort_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Testimonial %r>' % self.author


class JobPosting(db.Model):
    __tablename__ = 'job_postings'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    slug = db.Column(db.String(180), unique=True, nullable=False, index=True)
    summary = db.Column(db.Text)
    responsibilities = db.Column(db.JSON, default=list)
    qualifications = db.Column(db.JSON, default=list)
    location = db.Column(db.String(128), default='Narok, Kenya')
    is_active = db.Column(db.Boolean, default=True, index=True)
    posted_at = db.Column(db.DateTime, default=utcnow)

    def __repr__(self):
        return '<JobPosting %r>' % self.title


class JobApplication(db.Model):
    __tablename__ = 'job_applications'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_postings.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(64))
    message = db.Column(db.Text)
    cv_filename = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=utcnow)

    job = db.relationship('JobPosting', backref=db.backref('applications', lazy='dynamic'))

    def __repr__(self):
        return '<JobApplication %r>' % self.name


class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(64))
    travellers = db.Column(db.String(64))
    destination = db.Column(db.String(160))
    subject = db.Column(db.String(128))
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=utcnow)

    def __repr__(self):
        return '<ContactMessage %r>' % self.name


class BookingRequest(db.Model):
    __tablename__ = 'booking_requests'

    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(32), default='package')
    item_id = db.Column(db.Integer)
    item_title = db.Column(db.String(160))
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(64))
    travellers = db.Column(db.Integer, default=1)
    travel_date = db.Column(db.Date)
    message = db.Column(db.Text)
    status = db.Column(db.String(32), default='new', index=True)
    created_at = db.Column(db.DateTime, default=utcnow)

    # Online payment (Visa / Mastercard via Flutterwave hosted checkout)
    amount = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(8))
    tx_ref = db.Column(db.String(64), unique=True, index=True)
    payment_status = db.Column(db.String(16), default='unpaid', index=True)
    flw_transaction_id = db.Column(db.String(64))
    paid_at = db.Column(db.DateTime)

    @property
    def is_paid(self):
        return self.payment_status == 'paid'

    def __repr__(self):
        return '<BookingRequest %r>' % self.item_title


class Subscriber(db.Model):
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utcnow)

    def __repr__(self):
        return '<Subscriber %r>' % self.email


class LegalPage(db.Model):
    """Editable policy / terms / cancellation content."""

    __tablename__ = 'legal_pages'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    hero_title = db.Column(db.String(160))
    hero_subtitle = db.Column(db.String(255))
    content = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)

    def __repr__(self):
        return '<LegalPage %r>' % self.slug


for _model in (Destination, Package, JobPosting):
    event.listen(_model, 'before_insert', _auto_slug)
