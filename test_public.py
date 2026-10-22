"""Tests for the public pages, forms and the JSON API."""
from app.models import (
    BookingRequest,
    ContactMessage,
    Destination,
    JobApplication,
    JobPosting,
    LegalPage,
    Package,
    Subscriber,
)


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'RemoteTravels' in response.data


def test_static_pages_render(client):
    for url in ('/about', '/destinations', '/packages', '/contacts', '/careers'):
        assert client.get(url).status_code == 200


def test_404_page(client):
    response = client.get('/this-page-does-not-exist')
    assert response.status_code == 404


def test_legacy_urls_redirect(client):
    for url in ('/about.html', '/packages.html', '/policy.html', '/terms.html'):
        response = client.get(url)
        assert response.status_code == 302


def test_destination_detail(client):
    from app.extensions import db
    destination = Destination(name='Test Safari', tag='Safari', description='A test',
                              price='$1,000', price_value=1000, duration_days=5,
                              location='Kenya', is_active=True)
    with client.application.app_context():
        db.session.add(destination)
        db.session.commit()
        slug = destination.slug

    assert client.get('/destinations/%s' % slug).status_code == 200


def test_package_detail(client):
    from app.extensions import db
    package = Package(name='Test Package', description='A test package', price='$900',
                      price_value=900, days=4, nights=3, is_active=True)
    with client.application.app_context():
        db.session.add(package)
        db.session.commit()
        slug = package.slug

    assert client.get('/packages/%s' % slug).status_code == 200


def test_contact_form_creates_message(client):
    response = client.post('/contacts', data={
        'name': 'Jane Traveller',
        'email': 'jane@example.com',
        'phone': '+254700000000',
        'travellers': '2',
        'destination': 'Maasai Mara',
        'subject': 'General Inquiry',
        'message': 'I would like to plan a trip.',
    }, follow_redirects=True)

    assert response.status_code == 200
    with client.application.app_context():
        assert ContactMessage.query.filter_by(email='jane@example.com').count() == 1


def test_contact_form_requires_fields(client):
    response = client.post('/contacts', data={'name': '', 'email': 'not-an-email'})
    assert response.status_code == 200
    with client.application.app_context():
        assert ContactMessage.query.count() == 0


def test_newsletter_subscribe(client):
    response = client.post('/newsletter/subscribe', data={'email': 'fan@example.com'},
                           follow_redirects=True)
    assert response.status_code == 200
    with client.application.app_context():
        assert Subscriber.query.filter_by(email='fan@example.com').count() == 1


def test_newsletter_rejects_bad_email(client):
    client.post('/newsletter/subscribe', data={'email': 'nope'}, follow_redirects=True)
    with client.application.app_context():
        assert Subscriber.query.count() == 0


def test_booking_request(client):
    response = client.post('/booking', data={
        'item_type': 'package',
        'item_title': 'African Safari',
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '+254700000001',
        'travellers': '3',
        'travel_date': '2026-12-01',
        'message': 'Window seat please.',
    }, follow_redirects=True)

    assert response.status_code == 200
    with client.application.app_context():
        booking = BookingRequest.query.first()
        assert booking is not None
        assert booking.email == 'john@example.com'


def test_job_application(client):
    from app.extensions import db
    job = JobPosting(title='Safari Guide', summary='Guide role',
                      responsibilities='Drive', qualifications='Experience',
                      location='Narok', is_active=True)
    with client.application.app_context():
        db.session.add(job)
        db.session.commit()
        slug = job.slug

    response = client.post('/careers/%s' % slug, data={
        'name': 'Peter Guide',
        'email': 'peter@example.com',
        'phone': '+254700000002',
        'message': 'I have ten years of experience.',
    }, follow_redirects=True)

    assert response.status_code == 200
    with client.application.app_context():
        assert JobApplication.query.filter_by(email='peter@example.com').count() == 1


def test_legal_page(client):
    from app.extensions import db
    page = LegalPage(slug='test-policy', title='Test Policy', content='<p>Hi</p>')
    with client.application.app_context():
        db.session.add(page)
        db.session.commit()

    assert client.get('/legal/test-policy').status_code == 200


def test_sitemap_and_robots(client):
    sitemap = client.get('/sitemap.xml')
    assert sitemap.status_code == 200
    assert b'<urlset' in sitemap.data

    robots = client.get('/robots.txt')
    assert robots.status_code == 200
    assert b'Sitemap' in robots.data


def test_api_destinations(client):
    response = client.get('/api/v1/destinations')
    assert response.status_code == 200
    assert response.is_json
    assert 'destinations' in response.get_json()


def test_api_destination_detail(client):
    from app.extensions import db
    destination = Destination(name='API Safari', tag='Safari', description='x',
                              highlights='[]', is_active=True)
    with client.application.app_context():
        db.session.add(destination)
        db.session.commit()
        destination_id = destination.id

    response = client.get('/api/v1/destinations/%d' % destination_id)
    assert response.status_code == 200
    assert response.get_json()['name'] == 'API Safari'


def test_api_packages_and_experiences(client):
    assert client.get('/api/v1/packages').status_code == 200
    assert client.get('/api/v1/experiences').status_code == 200
