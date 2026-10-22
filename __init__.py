from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import forms, views  # noqa: E402,F401


def admin_stats():
    """Counters used by the dashboard and the sidebar badge."""
    from ..models import (
        BookingRequest,
        ContactMessage,
        Destination,
        Experience,
        JobApplication,
        JobPosting,
        Package,
        Subscriber,
    )

    return {
        'destinations': Destination.query.count(),
        'packages': Package.query.count(),
        'experiences': Experience.query.count(),
        'jobs': JobPosting.query.filter_by(is_active=True).count(),
        'messages': ContactMessage.query.count(),
        'unread_messages': ContactMessage.query.filter_by(is_read=False).count(),
        'bookings': BookingRequest.query.count(),
        'applications': JobApplication.query.count(),
        'subscribers': Subscriber.query.count(),
    }


@admin.app_context_processor
def inject_admin_stats():
    """Expose the dashboard counters to every admin template."""
    try:
        stats = admin_stats()
    except Exception:  # pragma: no cover - database not ready yet
        stats = {}

    return dict(stats=stats)
