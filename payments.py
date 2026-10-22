"""Flutterwave hosted-checkout helpers (Visa, Mastercard and M-Pesa).

The customer never types card details on our site: we ask Flutterwave for a
payment link, redirect the customer there, and then *verify* the result with
Flutterwave from the server before marking a booking as paid.
"""
import secrets
from decimal import ROUND_HALF_UP, Decimal

import requests
from flask import current_app

from .models import Destination, Package


class PaymentError(Exception):
    """Raised when we cannot start or verify a payment."""


def payments_enabled():
    return bool(current_app.config.get('FLW_SECRET_KEY'))


def new_tx_ref():
    return 'RT-%s' % secrets.token_hex(8).upper()


def lookup_item(item_type, item_id):
    """Return the Package/Destination being booked (looked up on the server)."""
    model = Destination if item_type == 'destination' else Package
    if not item_id:
        return None
    return model.query.filter_by(id=item_id, is_active=True).first()


def compute_amount(item, travellers):
    """Price x travellers x deposit%. Always computed on the server."""
    unit = Decimal(item.price_value or 0)
    percent = Decimal(current_app.config['PAYMENT_DEPOSIT_PERCENT']) / Decimal(100)
    total = unit * Decimal(max(int(travellers or 1), 1)) * percent
    return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def _headers():
    return {'Authorization': 'Bearer %s' % current_app.config['FLW_SECRET_KEY'],
            'Content-Type': 'application/json'}


def create_payment_link(booking, redirect_url):
    """Ask Flutterwave for a hosted checkout link for this booking."""
    payload = {
        'tx_ref': booking.tx_ref,
        'amount': str(booking.amount),
        'currency': booking.currency,
        'redirect_url': redirect_url,
        'payment_options': 'card,mpesa',
        'customer': {'email': booking.email, 'name': booking.name,
                     'phonenumber': booking.phone or ''},
        'customizations': {'title': current_app.config['SITE_NAME'],
                           'description': (booking.item_title or 'Trip booking')[:100]},
        'meta': {'booking_id': booking.id},
    }
    try:
        response = requests.post('%s/payments' % current_app.config['FLW_BASE_URL'],
                                 json=payload, headers=_headers(), timeout=20)
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        current_app.logger.error('Flutterwave request failed: %s', exc)
        raise PaymentError('Could not reach the payment provider.') from exc

    link = (data.get('data') or {}).get('link')
    if response.status_code != 200 or data.get('status') != 'success' or not link:
        current_app.logger.error('Flutterwave rejected payment: %s', data)
        raise PaymentError('The payment provider rejected the request.')
    return link


def verify_transaction(transaction_id):
    """Fetch the real transaction from Flutterwave (never trust the redirect)."""
    try:
        response = requests.get('%s/transactions/%s/verify' % (
            current_app.config['FLW_BASE_URL'], transaction_id),
            headers=_headers(), timeout=20)
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        current_app.logger.error('Flutterwave verify failed: %s', exc)
        raise PaymentError('Could not verify the payment right now.') from exc
    if response.status_code != 200 or data.get('status') != 'success':
        raise PaymentError('Payment could not be verified.')
    return data['data']


def transaction_matches(booking, txn):
    """True only if a verified transaction really pays for this booking."""
    try:
        paid_enough = Decimal(str(txn.get('amount'))) >= Decimal(str(booking.amount))
    except Exception:
        return False
    return (txn.get('status') == 'successful'
            and txn.get('tx_ref') == booking.tx_ref
            and str(txn.get('currency', '')).upper() == (booking.currency or '').upper()
            and paid_enough)
