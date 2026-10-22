"""Tests for the Flutterwave payment flow (the network is always mocked)."""
from unittest.mock import patch

import pytest

from app import payments
from app.extensions import db
from app.models import BookingRequest, Package


@pytest.fixture()
def paid_app(app):
    app.config['FLW_SECRET_KEY'] = 'FLWSECK_TEST-xxxx'
    app.config['FLW_SECRET_HASH'] = 'my-secret-hash'
    app.config['PAYMENT_CURRENCY'] = 'USD'
    app.config['PAYMENT_DEPOSIT_PERCENT'] = 100
    return app


@pytest.fixture()
def package(paid_app):
    item = Package(name='Mara Escape', slug='mara-escape', price='$1,000', price_value=1000,
                   days=3, nights=2, is_active=True)
    db.session.add(item)
    db.session.commit()
    return item


class FakeResponse:
    def __init__(self, data, status_code=200):
        self._data, self.status_code = data, status_code

    def json(self):
        return self._data


def _post_booking(client, package, **extra):
    data = {'item_type': 'package', 'item_id': package.id, 'item_title': 'HACKED TITLE',
            'name': 'Amina', 'email': 'amina@example.com', 'travellers': 2, 'action': 'pay'}
    data.update(extra)
    return client.post('/booking', data=data)


def test_pay_now_redirects_to_flutterwave_and_charges_server_side_price(client, package):
    link = {'status': 'success', 'data': {'link': 'https://checkout.flutterwave.com/v3/hosted/pay/abc'}}
    with patch('app.payments.requests.post', return_value=FakeResponse(link)) as post:
        response = _post_booking(client, package)
    assert response.status_code == 302
    assert response.headers['Location'] == link['data']['link']
    sent = post.call_args.kwargs['json']
    assert sent['amount'] == '2000.00'          # 1000 x 2 travellers, computed on the server
    assert sent['currency'] == 'USD'
    booking = BookingRequest.query.one()
    assert booking.payment_status == 'pending'
    assert booking.item_title == 'Mara Escape'  # client-sent title is ignored
    assert booking.tx_ref == sent['tx_ref']


def test_pay_now_disabled_without_keys(client, package, paid_app):
    paid_app.config['FLW_SECRET_KEY'] = ''
    response = _post_booking(client, package)
    assert response.status_code == 302
    assert BookingRequest.query.count() == 0


def test_provider_failure_keeps_the_booking_request(client, package):
    with patch('app.payments.requests.post', return_value=FakeResponse({'status': 'error'}, 400)):
        response = _post_booking(client, package)
    assert response.status_code == 302
    booking = BookingRequest.query.one()
    assert booking.payment_status == 'unpaid'


def _pending_booking(client, package):
    link = {'status': 'success', 'data': {'link': 'https://checkout.flutterwave.com/x'}}
    with patch('app.payments.requests.post', return_value=FakeResponse(link)):
        _post_booking(client, package)
    return BookingRequest.query.one()


def _verified(booking, **over):
    txn = {'id': 555, 'status': 'successful', 'tx_ref': booking.tx_ref,
           'amount': float(booking.amount), 'currency': 'USD'}
    txn.update(over)
    return FakeResponse({'status': 'success', 'data': txn})


def test_callback_marks_paid_after_verification(client, package):
    booking = _pending_booking(client, package)
    with patch('app.payments.requests.get', return_value=_verified(booking)):
        response = client.get('/payment/callback', query_string={
            'status': 'successful', 'tx_ref': booking.tx_ref, 'transaction_id': '555'})
    assert response.status_code == 200
    assert b'Payment received' in response.data
    db.session.refresh(booking)
    assert booking.is_paid and booking.flw_transaction_id == '555'


def test_callback_rejects_underpayment(client, package):
    booking = _pending_booking(client, package)
    with patch('app.payments.requests.get', return_value=_verified(booking, amount=1)):
        response = client.get('/payment/callback', query_string={
            'status': 'successful', 'tx_ref': booking.tx_ref, 'transaction_id': '555'})
    assert b'Payment unsuccessful' in response.data
    db.session.refresh(booking)
    assert not booking.is_paid


def test_callback_cannot_be_faked_with_url_params(client, package):
    booking = _pending_booking(client, package)
    with patch('app.payments.requests.get', return_value=FakeResponse({'status': 'error'}, 400)):
        response = client.get('/payment/callback', query_string={
            'status': 'successful', 'tx_ref': booking.tx_ref, 'transaction_id': '999'})
    assert b'Payment received' not in response.data
    db.session.refresh(booking)
    assert not booking.is_paid


def test_callback_unknown_reference_is_404(client, paid_app):
    assert client.get('/payment/callback', query_string={'tx_ref': 'nope'}).status_code == 404


def test_webhook_requires_correct_hash(client, package):
    response = client.post('/payment/webhook', json={'event': 'charge.completed'},
                           headers={'verif-hash': 'wrong'})
    assert response.status_code == 401


def test_webhook_marks_paid_and_is_idempotent(client, package):
    booking = _pending_booking(client, package)
    body = {'event': 'charge.completed', 'data': {'id': 555, 'tx_ref': booking.tx_ref}}
    headers = {'verif-hash': 'my-secret-hash'}
    with patch('app.payments.requests.get', return_value=_verified(booking)):
        assert client.post('/payment/webhook', json=body, headers=headers).status_code == 200
        assert client.post('/payment/webhook', json=body, headers=headers).status_code == 200
    db.session.refresh(booking)
    assert booking.is_paid


def test_plain_request_still_works_without_payment(client, package):
    response = client.post('/booking', data={
        'item_type': 'package', 'item_id': package.id, 'item_title': 'Mara Escape',
        'name': 'Joe', 'email': 'joe@example.com', 'travellers': 1})
    assert response.status_code == 302
    booking = BookingRequest.query.one()
    assert booking.tx_ref is None and booking.payment_status in (None, 'unpaid')


def test_compute_amount_with_deposit(paid_app, package):
    paid_app.config['PAYMENT_DEPOSIT_PERCENT'] = 30
    with paid_app.test_request_context():
        assert str(payments.compute_amount(package, 2)) == '600.00'
