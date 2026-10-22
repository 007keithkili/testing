#!/usr/bin/env python3
"""Entry point for the RemoteTravels Flask application.

Usage:
    flask --app manage.py init-db          # create tables + load starter content
    flask --app manage.py create-admin     # create an administrator account
    flask --app manage.py test             # run the test suite
    flask --app manage.py run              # start the development server
"""
import os
import sys

from app import create_app, db
from app.models import (
    BookingRequest,
    ContactMessage,
    Destination,
    Experience,
    Feature,
    JobApplication,
    JobPosting,
    LegalPage,
    Package,
    Permission,
    Role,
    Service,
    SiteSetting,
    Subscriber,
    Testimonial,
    Touchpoint,
    User,
    Wildlife,
)

app = create_app(os.environ.get('FLASK_CONFIG', 'default'))


@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app, db=db,
        User=User, Role=Role, Permission=Permission,
        Destination=Destination, Package=Package, Experience=Experience,
        Wildlife=Wildlife, Service=Service, Feature=Feature,
        Touchpoint=Touchpoint, Testimonial=Testimonial,
        JobPosting=JobPosting, JobApplication=JobApplication,
        ContactMessage=ContactMessage, BookingRequest=BookingRequest,
        Subscriber=Subscriber, LegalPage=LegalPage, SiteSetting=SiteSetting,
    )


@app.cli.command('test')
def test():
    """Run the test suite."""
    import pytest

    sys.exit(pytest.main(['-q', 'tests']))


if __name__ == '__main__':
    app.run(host=os.environ.get('HOST', '0.0.0.0'), port=int(os.environ.get('PORT', 5000)))
