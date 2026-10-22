import hmac
import os
import re
from datetime import datetime, timezone

from flask import (
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_mail import Message

from . import main
from .forms import BookingForm, ContactForm, JobApplicationForm, NewsletterForm
from .. import payments
from ..extensions import csrf, db, mail
from ..models import (
    BookingRequest,
    ContactMessage,
    Destination,
    Experience,
    Feature,
    JobApplication,
    JobPosting,
    LegalPage,
    Package,
    Service,
    SiteSetting,
    Subscriber,
    Testimonial,
    Touchpoint,
    Wildlife,
)

LEGACY_SLUGS = {
    'index.html': 'index',
    'about.html': 'about',
    'destinations.html': 'destinations',
    'packages.html': 'packages',
    'contacts.html': 'contacts',
    'careers.html': 'careers',
    'policy.html': 'privacy',
    'terms.html': 'terms',
    'cancellationpolicy.html': 'cancellation',
}


@main.route('/')
def index():
    destinations = (Destination.query
                    .filter_by(is_active=True, is_featured=True)
                    .order_by(Destination.sort_order, Destination.id)
                    .all())
    packages = (Package.query
                .filter_by(is_active=True, is_featured=True)
                .order_by(Package.sort_order, Package.id)
                .all())
    wildlife = Wildlife.query.order_by(Wildlife.sort_order, Wildlife.id).all()
    services = Service.query.order_by(Service.sort_order, Service.id).all()
    testimonials = Testimonial.query.order_by(Testimonial.sort_order, Testimonial.id).all()

    return render_template('index.html', destinations=destinations, packages=packages,
                           wildlife=wildlife, services=services, testimonials=testimonials)


@main.route('/about')
def about():
    features = Feature.query.order_by(Feature.sort_order, Feature.id).all()
    touchpoints = Touchpoint.query.order_by(Touchpoint.sort_order, Touchpoint.id).all()
    return render_template('about.html', features=features, touchpoints=touchpoints)


@main.route('/destinations')
def destinations():
    tag = request.args.get('tag', '').strip()
    query = Destination.query.filter_by(is_active=True)
    if tag:
        query = query.filter(Destination.tag == tag)
    items = query.order_by(Destination.sort_order, Destination.id).all()
    tags = [row[0] for row in db.session.query(Destination.tag).distinct()
            .order_by(Destination.tag).all()]
    return render_template('destinations.html', destinations=items, tags=tags, active_tag=tag)


@main.route('/destinations/<slug>')
def destination_detail(slug):
    item = Destination.query.filter_by(slug=slug, is_active=True).first_or_404()
    similar = (Destination.query
               .filter(Destination.tag == item.tag, Destination.id != item.id, Destination.is_active.is_(True))
               .order_by(Destination.sort_order)
               .limit(4).all())
    form = BookingForm()
    return render_template('destination_detail.html', destination=item, similar=similar, form=form)


@main.route('/packages')
def packages():
    items = (Package.query.filter_by(is_active=True)
             .order_by(Package.sort_order, Package.id).all())
    experiences = (Experience.query.filter_by(is_active=True)
                   .order_by(Experience.sort_order, Experience.id).all())

    labels = []
    for package in items:
        for label in (package.comparison or {}):
            if label not in labels:
                labels.append(label)
    comparison_rows = [{'label': label,
                        'values': [(package.comparison or {}).get(label, '-') for package in items]}
                       for label in labels]

    return render_template('packages.html', packages=items, experiences=experiences,
                           comparison_rows=comparison_rows)


@main.route('/packages/<slug>')
def package_detail(slug):
    item = Package.query.filter_by(slug=slug, is_active=True).first_or_404()
    form = BookingForm()
    return render_template('package_detail.html', package=item, form=form)


@main.route('/careers')
def careers():
    jobs = (JobPosting.query.filter_by(is_active=True)
            .order_by(JobPosting.posted_at.desc(), JobPosting.id.desc()).all())
    return render_template('careers.html', jobs=jobs)


@main.route('/careers/<slug>', methods=['GET', 'POST'])
def job_detail(slug):
    job = JobPosting.query.filter_by(slug=slug).first_or_404()
    form = JobApplicationForm()
    if form.validate_on_submit():
        cv_filename = None
        cv = form.cv.data
        if cv and cv.filename:
            extension = cv.filename.rsplit('.', 1)[-1].lower()
            if extension not in current_app.config['ALLOWED_UPLOAD_EXTENSIONS']:
                flash('That file type is not allowed.', 'danger')
                return redirect(url_for('main.job_detail', slug=job.slug))
            safe_name = re.sub(r'[^A-Za-z0-9_.-]', '_', cv.filename)
            cv_filename = '%s-%s' % (job.slug, safe_name)
            cv.save(os.path.join(current_app.config['UPLOAD_FOLDER'], cv_filename))

        application = JobApplication(job=job, name=form.name.data, email=form.email.data,
                                     phone=form.phone.data, message=form.message.data,
                                     cv_filename=cv_filename)
        db.session.add(application)
        db.session.commit()
        _notify_admin('New job application: %s' % job.title,
                      'A new application was received for the %s role.' % job.title)
        flash('Thank you! Your application for %s has been received.' % job.title, 'success')
        return redirect(url_for('main.careers'))
    return render_template('job_detail.html', job=job, form=form)


@main.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(name=form.name.data, email=form.email.data,
                                 phone=form.phone.data, travellers=form.travellers.data,
                                 destination=form.destination.data, subject=form.subject.data,
                                 message=form.message.data)
        db.session.add(message)
        db.session.commit()
        _notify_admin('New website enquiry: %s' % form.subject.data,
                      '%s <%s> sent a %s enquiry.' % (form.name.data, form.email.data,
                                                       form.subject.data.lower()))
        flash('Thank you! Our travel experts will get back to you within 24 hours.', 'success')
        return redirect(url_for('main.contacts'))
    return render_template('contacts.html', form=form)


@main.route('/legal/<slug>')
def legal(slug):
    page = LegalPage.query.filter_by(slug=slug).first_or_404()
    return render_template('legal.html', page=page)


@main.route('/newsletter/subscribe', methods=['POST'])
def subscribe():
    form = NewsletterForm()
    if not form.validate_on_submit():
        flash('Please enter a valid email address.', 'danger')
        return redirect(request.referrer or url_for('main.index'))

    email = form.email.data.strip().lower()
    subscriber = Subscriber.query.filter_by(email=email).first()
    if subscriber is None:
        db.session.add(Subscriber(email=email))
        db.session.commit()
        flash('Welcome aboard! Check your inbox for travel inspiration.', 'success')
    else:
        if not subscriber.is_active:
            subscriber.is_active = True
            db.session.commit()
            flash('You are subscribed again. Welcome back!', 'success')
        else:
            flash('You are already on the list. See you on the next adventure!', 'warning')
    return redirect(request.referrer or url_for('main.index'))


@main.route('/booking', methods=['POST'])
def booking():
    form = BookingForm()
    if not form.validate_on_submit():
        flash('Please complete the booking request form.', 'danger')
        return redirect(request.referrer or url_for('main.packages'))

    pay_now = request.form.get('action') == 'pay'
    item_type = form.item_type.data or 'package'
    item_title = form.item_title.data
    amount = None

    if pay_now:
        if not payments.payments_enabled():
            flash('Online payment is not available right now. Please send a booking request instead.', 'danger')
            return redirect(request.referrer or url_for('main.packages'))
        item = payments.lookup_item(item_type, form.item_id.data)
        if item is None or not item.price_value:
            flash('This trip cannot be paid for online. Please send a booking request instead.', 'danger')
            return redirect(request.referrer or url_for('main.packages'))
        item_title = item.name
        amount = payments.compute_amount(item, form.travellers.data or 1)

    booking_request = BookingRequest(
        item_type=item_type,
        item_id=form.item_id.data,
        item_title=item_title,
        name=form.name.data,
        email=form.email.data,
        phone=form.phone.data,
        travellers=form.travellers.data or 1,
        travel_date=form.travel_date.data,
        message=form.message.data,
    )

    if pay_now:
        booking_request.amount = amount
        booking_request.currency = current_app.config['PAYMENT_CURRENCY']
        booking_request.tx_ref = payments.new_tx_ref()
        booking_request.payment_status = 'pending'

    db.session.add(booking_request)
    db.session.commit()

    if pay_now:
        try:
            link = payments.create_payment_link(
                booking_request, url_for('main.payment_callback', _external=True))
        except payments.PaymentError:
            booking_request.payment_status = 'unpaid'
            db.session.commit()
            _notify_admin('Booking request (payment not started): %s' % item_title,
                          '%s requested a booking for %s but the payment could not be started.'
                          % (form.name.data, item_title))
            flash('We could not start the payment. Your booking request was saved and our team will contact you.',
                  'warning')
            return redirect(request.referrer or url_for('main.packages'))
        return redirect(link)

    _notify_admin('New booking request: %s' % (form.item_title.data or 'Custom tour'),
                  '%s requested a booking for %s.' % (form.name.data, form.item_title.data))
    flash('Your booking request is in. We will confirm availability shortly.', 'success')
    return redirect(request.referrer or url_for('main.packages'))


def _apply_verified_payment(booking_request, txn):
    """Mark a booking as paid once Flutterwave has confirmed the transaction.

    Safe to call more than once (the redirect and the webhook both call it).
    """
    if booking_request.is_paid:
        return True
    if not payments.transaction_matches(booking_request, txn):
        return False
    booking_request.payment_status = 'paid'
    booking_request.status = 'paid'
    booking_request.flw_transaction_id = str(txn.get('id'))
    booking_request.paid_at = datetime.now(timezone.utc)
    db.session.commit()
    _notify_admin('PAID booking: %s' % booking_request.item_title,
                  '%s paid %s %s for %s (ref %s).' % (
                      booking_request.name, booking_request.amount, booking_request.currency,
                      booking_request.item_title, booking_request.tx_ref))
    _email_customer_receipt(booking_request)
    return True


def _email_customer_receipt(booking_request):
    try:
        message = Message(
            subject='Payment received - %s' % booking_request.item_title,
            recipients=[booking_request.email],
            body=('Hi %s,\n\nThank you! We received your payment of %s %s for %s '
                  '(reference %s).\n\nOur travel team will contact you shortly to confirm '
                  'your itinerary.\n\nRemoteTravels' % (
                      booking_request.name, booking_request.amount, booking_request.currency,
                      booking_request.item_title, booking_request.tx_ref)),
            sender=current_app.config.get('BLOGGING_MAIL_SENDER'))
        mail.send(message)
    except Exception:  # pragma: no cover - mail server may be unavailable
        current_app.logger.warning('Unable to send receipt to %s', booking_request.email)


@main.route('/payment/callback')
def payment_callback():
    """Flutterwave sends the customer back here after checkout."""
    tx_ref = request.args.get('tx_ref', '')
    booking_request = BookingRequest.query.filter_by(tx_ref=tx_ref).first() if tx_ref else None
    if booking_request is None:
        abort(404)

    outcome = 'pending'
    flw_status = request.args.get('status', '')
    transaction_id = request.args.get('transaction_id', '')

    if booking_request.is_paid:
        outcome = 'success'
    elif flw_status in ('successful', 'completed') and transaction_id:
        try:
            txn = payments.verify_transaction(transaction_id)
            outcome = 'success' if _apply_verified_payment(booking_request, txn) else 'failed'
        except payments.PaymentError:
            outcome = 'pending'  # the webhook will still confirm it
    elif flw_status == 'cancelled':
        outcome = 'cancelled'
    else:
        outcome = 'failed'

    if outcome in ('failed', 'cancelled') and not booking_request.is_paid:
        booking_request.payment_status = outcome
        db.session.commit()

    return render_template('payment_result.html', booking=booking_request, outcome=outcome)


@main.route('/payment/webhook', methods=['POST'])
@csrf.exempt
def payment_webhook():
    """Server-to-server confirmation from Flutterwave (works even if the customer closes the tab)."""
    expected = current_app.config.get('FLW_SECRET_HASH') or ''
    received = request.headers.get('verif-hash', '')
    if not expected or not hmac.compare_digest(received, expected):
        abort(401)

    payload = request.get_json(silent=True) or {}
    data = payload.get('data') or {}
    tx_ref = data.get('tx_ref')
    transaction_id = data.get('id')
    if payload.get('event') != 'charge.completed' or not tx_ref or not transaction_id:
        return jsonify(status='ignored'), 200

    booking_request = BookingRequest.query.filter_by(tx_ref=tx_ref).first()
    if booking_request is None:
        return jsonify(status='unknown reference'), 200

    try:
        txn = payments.verify_transaction(transaction_id)
    except payments.PaymentError:
        return jsonify(status='verification failed'), 500  # Flutterwave will retry
    _apply_verified_payment(booking_request, txn)
    return jsonify(status='ok'), 200


@main.route('/sitemap.xml')
def sitemap():
    urls = [('/', 'daily'), ('/about', 'monthly'), ('/destinations', 'weekly'),
            ('/packages', 'weekly'), ('/careers', 'weekly'), ('/contacts', 'monthly')]
    base = current_app.config['SITE_URL'].rstrip('/')

    items = []
    for path, frequency in urls:
        items.append('<url><loc>%s%s</loc><changefreq>%s</changefreq></url>' % (base, path, frequency))
    for destination in Destination.query.filter_by(is_active=True).all():
        items.append('<url><loc>%s/destinations/%s</loc></url>' % (base, destination.slug))
    for package in Package.query.filter_by(is_active=True).all():
        items.append('<url><loc>%s/packages/%s</loc></url>' % (base, package.slug))
    for job in JobPosting.query.filter_by(is_active=True).all():
        items.append('<url><loc>%s/careers/%s</loc></url>' % (base, job.slug))
    for page in LegalPage.query.all():
        items.append('<url><loc>%s/legal/%s</loc></url>' % (base, page.slug))

    body = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + '\n'.join(items) + '\n</urlset>')
    response = current_app.response_class(body, mimetype='application/xml')
    return response


@main.route('/robots.txt')
def robots():
    body = ('User-agent: *\n'
            'Disallow: /admin\n'
            'Disallow: /auth\n'
            'Allow: /\n\n'
            'Sitemap: %s/sitemap.xml\n' % current_app.config['SITE_URL'].rstrip('/'))
    return current_app.response_class(body, mimetype='text/plain')


@main.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')


@main.route('/<legacy>.html')
def legacy_page(legacy):
    """Keep the old static URLs working for inbound links and search engines."""
    slug = LEGACY_SLUGS.get('%s.html' % legacy.lower())
    if slug is None:
        abort(404)
    if slug == 'index':
        return redirect(url_for('main.index'))
    if slug == 'about':
        return redirect(url_for('main.about'))
    if slug == 'destinations':
        return redirect(url_for('main.destinations'))
    if slug == 'packages':
        return redirect(url_for('main.packages'))
    if slug == 'contacts':
        return redirect(url_for('main.contacts'))
    if slug == 'careers':
        return redirect(url_for('main.careers'))
    return redirect(url_for('main.legal', slug=slug))


def _notify_admin(subject, body):
    """Send a short notification to the site administrator (best effort)."""
    admin = SiteSetting.get('admin_email') or current_app.config.get('BLOGGING_ADMIN_EMAIL')
    if not admin:
        return
    try:
        message = Message(subject=subject, recipients=[admin], body=body,
                          sender=current_app.config.get('BLOGGING_MAIL_SENDER'))
        mail.send(message)
    except Exception:  # pragma: no cover - mail server may be unavailable
        current_app.logger.warning('Unable to send notification email: %s', subject)
