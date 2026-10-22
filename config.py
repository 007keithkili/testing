import os

from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(base_dir, 'instance')


class Config:
    """Settings shared by every environment."""

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hardtoguessstring'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # RemoteTravels public site
    SITE_NAME = 'RemoteTravels'
    SITE_URL = os.environ.get('SITE_URL', 'https://www.remotetravels.co.ke')
    API_BASE = os.environ.get('API_BASE', '/api/v1')
    BLOGGING_MAIL_PREFIX = '[RemoteTravels]'
    BLOGGING_MAIL_SENDER = os.environ.get('MAIL_SENDER', 'info@remotetravels.co.ke')
    BLOGGING_ADMIN_EMAIL = os.environ.get('MAIL_ADMIN')
    BLOGGING_ADMIN = os.environ.get('MAIL_ADMIN')
    BLOGGING_MAIL_SUBJECT_PREFIX = '[RemoteTravels]'
    BLOGGING_POSTS_PER_PAGE = 10
    BLOGGING_COMMENTS_PER_PAGE = 5

    # Uploaded CVs / itineraries
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(instance_dir, 'uploads'))
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    ALLOWED_UPLOAD_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'}

    # Card payments (Flutterwave hosted checkout: Visa, Mastercard, M-Pesa)
    FLW_SECRET_KEY = os.environ.get('FLW_SECRET_KEY', '')
    FLW_SECRET_HASH = os.environ.get('FLW_SECRET_HASH', '')
    FLW_BASE_URL = os.environ.get('FLW_BASE_URL', 'https://api.flutterwave.com/v3')
    PAYMENT_CURRENCY = os.environ.get('PAYMENT_CURRENCY', 'USD')
    # Percentage of the trip price charged online (100 = full amount, 30 = 30% deposit)
    PAYMENT_DEPOSIT_PERCENT = int(os.environ.get('PAYMENT_DEPOSIT_PERCENT', 100))

    @staticmethod
    def init_app(app):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 25))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'false').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///' + os.path.join(instance_dir, 'data-dev.sqlite'))


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TESTING_DATABASE_URI', 'sqlite:///' + os.path.join(instance_dir, 'data-test.sqlite'))
    SERVER_NAME = 'localhost'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///' + os.path.join(instance_dir, 'data.sqlite'))
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
