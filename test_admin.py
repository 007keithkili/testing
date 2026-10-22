"""Tests for authentication and the admin panel."""
from app.extensions import db
from app.models import (
    ContactMessage,
    Destination,
    LegalPage,
    Package,
    Role,
    SiteSetting,
    User,
)


def test_login_page(client):
    assert client.get('/auth/login').status_code == 200


def test_login_with_bad_password(client, admin):
    response = client.post('/auth/login',
                           data={'username': 'admin', 'password': 'wrong'},
                           follow_redirects=True)
    assert response.status_code == 200
    with client.application.app_context():
        assert User.query.filter_by(username='admin').first().is_admin


def test_login_and_logout(client, admin):
    response = client.post('/auth/login',
                           data={'username': 'admin', 'password': 'secret123'},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome back' in response.data

    client.get('/auth/logout', follow_redirects=True)
    response = client.get('/admin/')
    assert response.status_code == 302


def test_admin_pages_require_login(client):
    for url in ('/admin/', '/admin/destinations', '/admin/packages', '/admin/jobs',
                '/admin/inquiries', '/admin/pages', '/admin/settings'):
        assert client.get(url).status_code == 302


def test_admin_dashboard(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200
    assert b'Dashboard' in response.data


def test_admin_list_pages(admin_client):
    for url in ('/admin/destinations', '/admin/packages', '/admin/jobs',
                '/admin/inquiries', '/admin/pages', '/admin/settings'):
        assert admin_client.get(url).status_code == 200


def test_admin_creates_destination(admin_client):
    response = admin_client.post('/admin/destinations/new', data={
        'name': 'Admin Safari',
        'tag': 'Safari',
        'description': 'Created from the admin panel',
        'highlights': 'Lions\nElephants',
        'price': '$1,500',
        'price_value': '1500',
        'duration_days': '6',
        'location': 'Kenya',
        'is_active': 'y',
    }, follow_redirects=True)
    assert response.status_code == 200

    with admin_client.application.app_context():
        destination = Destination.query.filter_by(name='Admin Safari').first()
        assert destination is not None
        assert destination.slug == 'admin-safari'
        assert destination.highlights == ['Lions', 'Elephants']


def test_admin_creates_package_with_comparison(admin_client):
    response = admin_client.post('/admin/packages/new', data={
        'name': 'Admin Package',
        'description': 'Test package',
        'price': '$1,000',
        'price_value': '1000',
        'days': '5',
        'nights': '4',
        'features': 'Safari drive\nHot air balloon',
        'comparison': 'Duration: 5 days\nGuide: Expert',
        'is_active': 'y',
    }, follow_redirects=True)
    assert response.status_code == 200

    with admin_client.application.app_context():
        package = Package.query.filter_by(name='Admin Package').first()
        assert package is not None
        assert package.comparison['Duration'] == '5 days'


def test_admin_edits_and_deletes_destination(admin_client):
    with admin_client.application.app_context():
        destination = Destination(name='Temporary', tag='Safari', is_active=True)
        db.session.add(destination)
        db.session.commit()
        destination_id = destination.id

    admin_client.post('/admin/destinations/%d/edit' % destination_id,
                      data={'name': 'Renamed', 'tag': 'Safari', 'is_active': 'y'},
                      follow_redirects=True)

    with admin_client.application.app_context():
        assert db.session.get(Destination, destination_id).name == 'Renamed'

    admin_client.post('/admin/destinations/%d/delete' % destination_id,
                      follow_redirects=True)
    with admin_client.application.app_context():
        assert db.session.get(Destination, destination_id) is None


def test_admin_updates_settings(admin_client):
    admin_client.post('/admin/settings', data={
        'company_name': 'RemoteTravels Ltd',
        'phone': '+254 700 000 000',
        'email': 'hello@remotetravels.co.ke',
    }, follow_redirects=True)

    with admin_client.application.app_context():
        assert SiteSetting.get('company_name') == 'RemoteTravels Ltd'


def test_admin_edits_legal_page(admin_client):
    with admin_client.application.app_context():
        page = LegalPage(slug='privacy', title='Privacy Policy', content='<p>Old</p>')
        db.session.add(page)
        db.session.commit()
        page_id = page.id

    admin_client.post('/admin/pages/%d/edit' % page_id,
                      data={'title': 'Privacy Policy', 'content': '<p>New</p>'},
                      follow_redirects=True)

    with admin_client.application.app_context():
        assert db.session.get(LegalPage, page_id).content == '<p>New</p>'


def test_admin_inquiries_listing(admin_client):
    with admin_client.application.app_context():
        db.session.add(ContactMessage(name='Visitor', email='v@example.com',
                                       subject='General Inquiry', message='Hello'))
        db.session.commit()

    response = admin_client.get('/admin/inquiries')
    assert response.status_code == 200
    assert b'Visitor' in response.data


def test_non_admin_cannot_reach_admin(client, app):
    with app.app_context():
        role = Role.query.filter_by(name='User').first()
        user = User(username='visitor', email='visitor@example.com',
                    role=role, confirmed=True)
        user.set_password('visitor123')
        db.session.add(user)
        db.session.commit()

    client.post('/auth/login', data={'username': 'visitor', 'password': 'visitor123'},
                follow_redirects=True)
    assert client.get('/admin/').status_code in (302, 403)
