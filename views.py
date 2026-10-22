from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from . import admin
from .forms import (
    DestinationForm,
    ExperienceForm,
    JobForm,
    LegalPageForm,
    PackageForm,
    SiteSettingsForm,
    lines_to_list,
)
from ..decorators import admin_required, editor_required
from ..extensions import db
from ..models import (
    BookingRequest,
    ContactMessage,
    Destination,
    Experience,
    JobApplication,
    JobPosting,
    LegalPage,
    Package,
    SiteSetting,
    Subscriber,
    slugify,
)

SETTINGS_FIELDS = [
    'company_name', 'tagline', 'phone', 'email', 'address', 'hours', 'whatsapp',
    'facebook', 'twitter', 'instagram', 'youtube', 'pinterest', 'admin_email',
    'hero_title', 'hero_subtitle', 'logo_url',
]


@admin.route('/')
@login_required
@admin_required
def dashboard():
    from . import admin_stats

    stats = admin_stats()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    recent_bookings = BookingRequest.query.order_by(BookingRequest.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats,
                           recent_messages=recent_messages, recent_bookings=recent_bookings)


# --------------------------------------------------------------------------- #
# Destinations
# --------------------------------------------------------------------------- #
@admin.route('/destinations')
@login_required
@editor_required
def destinations():
    items = Destination.query.order_by(Destination.sort_order, Destination.id).all()
    return render_template('admin/destinations.html', destinations=items)


@admin.route('/destinations/new', methods=['GET', 'POST'])
@login_required
@editor_required
def new_destination():
    form = DestinationForm()
    if form.validate_on_submit():
        item = Destination()
        _fill_destination(form, item)
        db.session.add(item)
        db.session.commit()
        flash('Destination created.', 'success')
        return redirect(url_for('admin.destinations'))
    return render_template('admin/destination_form.html', form=form, item=None)


@admin.route('/destinations/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@editor_required
def edit_destination(id):
    item = db.get_or_404(Destination, id)
    form = DestinationForm(obj=item)
    if request.method == 'POST' and form.validate_on_submit():
        _fill_destination(form, item)
        db.session.commit()
        flash('Destination updated.', 'success')
        return redirect(url_for('admin.destinations'))
    if request.method == 'GET':
        form.highlights.data = '\n'.join(item.highlights or [])
    return render_template('admin/destination_form.html', form=form, item=item)


@admin.route('/destinations/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_destination(id):
    item = db.get_or_404(Destination, id)
    db.session.delete(item)
    db.session.commit()
    flash('Destination deleted.', 'success')
    return redirect(url_for('admin.destinations'))


def _fill_destination(form, item):
    item.name = form.name.data
    item.slug = slugify(form.slug.data or form.name.data)
    item.tag = form.tag.data
    item.image_url = form.image_url.data
    item.description = form.description.data
    item.highlights = lines_to_list(form.highlights.data)
    item.price = form.price.data
    item.price_value = form.price_value.data or 0
    item.duration_days = form.duration_days.data or 1
    item.location = form.location.data
    item.sort_order = form.sort_order.data or 0
    item.is_featured = form.is_featured.data
    item.is_active = form.is_active.data
    return item


# --------------------------------------------------------------------------- #
# Packages
# --------------------------------------------------------------------------- #
@admin.route('/packages')
@login_required
@editor_required
def packages():
    items = Package.query.order_by(Package.sort_order, Package.id).all()
    experiences = Experience.query.order_by(Experience.sort_order, Experience.id).all()
    return render_template('admin/packages.html', packages=items, experiences=experiences)


@admin.route('/packages/new', methods=['GET', 'POST'])
@login_required
@editor_required
def new_package():
    form = PackageForm()
    if form.validate_on_submit():
        item = Package()
        _fill_package(form, item)
        db.session.add(item)
        db.session.commit()
        flash('Package created.', 'success')
        return redirect(url_for('admin.packages'))
    return render_template('admin/package_form.html', form=form, item=None)


@admin.route('/packages/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@editor_required
def edit_package(id):
    item = db.get_or_404(Package, id)
    form = PackageForm(obj=item)
    if request.method == 'POST' and form.validate_on_submit():
        _fill_package(form, item)
        db.session.commit()
        flash('Package updated.', 'success')
        return redirect(url_for('admin.packages'))
    if request.method == 'GET':
        form.features.data = '\n'.join(item.features or [])
        form.tags.data = ', '.join(item.tags or [])
        form.comparison.data = '\n'.join('%s: %s' % (label, value)
                                          for label, value in (item.comparison or {}).items())
    return render_template('admin/package_form.html', form=form, item=item)


@admin.route('/packages/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_package(id):
    item = db.get_or_404(Package, id)
    db.session.delete(item)
    db.session.commit()
    flash('Package deleted.', 'success')
    return redirect(url_for('admin.packages'))


def _comparison_dict(value):
    """Parse "Label: Value" lines into a dictionary."""
    result = {}
    for line in lines_to_list(value):
        if ':' in line:
            label, item = line.split(':', 1)
        else:
            label, item = line, ''
        result[label.strip()] = item.strip()
    return result


def _fill_package(form, item):
    item.name = form.name.data
    item.slug = slugify(form.slug.data or form.name.data)
    item.tagline = form.tagline.data
    item.description = form.description.data
    item.image_url = form.image_url.data
    item.price = form.price.data
    item.price_value = form.price_value.data or 0
    item.days = form.days.data or 1
    item.nights = form.nights.data or 0
    item.features = lines_to_list(form.features.data)
    item.tags = [tag.strip() for tag in (form.tags.data or '').split(',') if tag.strip()]
    item.comparison = _comparison_dict(form.comparison.data)
    item.highlight = form.highlight.data
    item.sort_order = form.sort_order.data or 0
    item.is_featured = form.is_featured.data
    item.is_active = form.is_active.data
    return item


# --------------------------------------------------------------------------- #
# Experiences
# --------------------------------------------------------------------------- #
@admin.route('/experiences/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@editor_required
def edit_experience(id):
    item = db.get_or_404(Experience, id)
    form = ExperienceForm(obj=item)
    if form.validate_on_submit():
        item.title = form.title.data
        item.duration = form.duration.data
        item.highlights = form.highlights.data
        item.price = form.price.data
        item.image_url = form.image_url.data
        item.sort_order = form.sort_order.data or 0
        item.is_active = form.is_active.data
        db.session.commit()
        flash('Experience updated.', 'success')
        return redirect(url_for('admin.packages'))
    return render_template('admin/experience_form.html', form=form, item=item)


@admin.route('/experiences/new', methods=['GET', 'POST'])
@login_required
@editor_required
def new_experience():
    form = ExperienceForm()
    if form.validate_on_submit():
        item = Experience(title=form.title.data, duration=form.duration.data,
                           highlights=form.highlights.data, price=form.price.data,
                           image_url=form.image_url.data, sort_order=form.sort_order.data or 0,
                           is_active=form.is_active.data)
        db.session.add(item)
        db.session.commit()
        flash('Experience created.', 'success')
        return redirect(url_for('admin.packages'))
    return render_template('admin/experience_form.html', form=form, item=None)


@admin.route('/experiences/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_experience(id):
    item = db.get_or_404(Experience, id)
    db.session.delete(item)
    db.session.commit()
    flash('Experience deleted.', 'success')
    return redirect(url_for('admin.packages'))


# --------------------------------------------------------------------------- #
# Jobs
# --------------------------------------------------------------------------- #
@admin.route('/jobs')
@login_required
@editor_required
def jobs():
    items = JobPosting.query.order_by(JobPosting.posted_at.desc()).all()
    return render_template('admin/jobs.html', jobs=items)


@admin.route('/jobs/new', methods=['GET', 'POST'])
@login_required
@editor_required
def new_job():
    form = JobForm()
    if form.validate_on_submit():
        item = JobPosting()
        _fill_job(form, item)
        db.session.add(item)
        db.session.commit()
        flash('Job posting created.', 'success')
        return redirect(url_for('admin.jobs'))
    return render_template('admin/job_form.html', form=form, item=None)


@admin.route('/jobs/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@editor_required
def edit_job(id):
    item = db.get_or_404(JobPosting, id)
    form = JobForm(obj=item)
    if request.method == 'POST' and form.validate_on_submit():
        _fill_job(form, item)
        db.session.commit()
        flash('Job posting updated.', 'success')
        return redirect(url_for('admin.jobs'))
    if request.method == 'GET':
        form.responsibilities.data = '\n'.join(item.responsibilities or [])
        form.qualifications.data = '\n'.join(item.qualifications or [])
    return render_template('admin/job_form.html', form=form, item=item)


@admin.route('/jobs/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_job(id):
    item = db.get_or_404(JobPosting, id)
    for application in item.applications.all():
        db.session.delete(application)
    db.session.delete(item)
    db.session.commit()
    flash('Job posting deleted.', 'success')
    return redirect(url_for('admin.jobs'))


@admin.route('/jobs/<int:id>/applications')
@login_required
@editor_required
def job_applications(id):
    item = db.get_or_404(JobPosting, id)
    return render_template('admin/job_applications.html', job=item,
                           applications=item.applications.order_by(JobApplication.created_at.desc()).all())


def _fill_job(form, item):
    item.title = form.title.data
    item.slug = slugify(form.slug.data or form.title.data)
    item.summary = form.summary.data
    item.responsibilities = lines_to_list(form.responsibilities.data)
    item.qualifications = lines_to_list(form.qualifications.data)
    item.location = form.location.data
    item.is_active = form.is_active.data
    return item


# --------------------------------------------------------------------------- #
# Inquiries
# --------------------------------------------------------------------------- #
@admin.route('/inquiries')
@login_required
@editor_required
def inquiries():
    tab = request.args.get('tab', 'messages')
    context = {
        'tab': tab,
        'messages': ContactMessage.query.order_by(ContactMessage.created_at.desc()).all(),
        'bookings': BookingRequest.query.order_by(BookingRequest.created_at.desc()).all(),
        'applications': JobApplication.query.order_by(JobApplication.created_at.desc()).all(),
        'subscribers': Subscriber.query.order_by(Subscriber.created_at.desc()).all(),
    }
    return render_template('admin/inquiries.html', **context)


@admin.route('/inquiries/message/<int:id>/toggle-read', methods=['POST'])
@login_required
@editor_required
def toggle_message_read(id):
    message = db.get_or_404(ContactMessage, id)
    message.is_read = not message.is_read
    db.session.commit()
    return redirect(url_for('admin.inquiries', tab='messages'))


@admin.route('/inquiries/message/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_message(id):
    db.session.delete(db.get_or_404(ContactMessage, id))
    db.session.commit()
    flash('Message deleted.', 'success')
    return redirect(url_for('admin.inquiries', tab='messages'))


@admin.route('/inquiries/booking/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_booking(id):
    db.session.delete(db.get_or_404(BookingRequest, id))
    db.session.commit()
    flash('Booking request deleted.', 'success')
    return redirect(url_for('admin.inquiries', tab='bookings'))


@admin.route('/inquiries/application/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_application(id):
    db.session.delete(db.get_or_404(JobApplication, id))
    db.session.commit()
    flash('Application deleted.', 'success')
    return redirect(url_for('admin.inquiries', tab='applications'))


# --------------------------------------------------------------------------- #
# Legal pages
# --------------------------------------------------------------------------- #
@admin.route('/pages')
@login_required
@editor_required
def pages():
    items = LegalPage.query.order_by(LegalPage.title).all()
    return render_template('admin/pages.html', pages=items)


@admin.route('/pages/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@editor_required
def edit_page(id):
    item = db.get_or_404(LegalPage, id)
    form = LegalPageForm(obj=item)
    if form.validate_on_submit():
        item.title = form.title.data
        item.hero_title = form.hero_title.data
        item.hero_subtitle = form.hero_subtitle.data
        item.content = form.content.data
        db.session.commit()
        flash('Page updated.', 'success')
        return redirect(url_for('admin.pages'))
    return render_template('admin/page_form.html', form=form, item=item)


# --------------------------------------------------------------------------- #
# Settings
# --------------------------------------------------------------------------- #
@admin.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def settings():
    form = SiteSettingsForm()
    if request.method == 'GET':
        current = SiteSetting.as_dict()
        for field in SETTINGS_FIELDS:
            if field in current:
                form[field].data = current[field]
    if form.validate_on_submit():
        for field in SETTINGS_FIELDS:
            SiteSetting.set(field, form[field].data or '')
        db.session.commit()
        flash('Settings saved.', 'success')
        return redirect(url_for('admin.settings'))
    return render_template('admin/settings.html', form=form)
