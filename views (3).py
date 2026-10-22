from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user
from urllib.parse import urljoin, urlparse

from . import auth
from .forms import LoginForm
from ..models import User


def _safe_redirect_target(target):
    """Only allow redirects that stay on this site."""
    if not target:
        return None
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    if redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc:
        return target
    return None


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_url = _safe_redirect_target(request.args.get('next'))
            flash('Welcome back, %s.' % (user.name or user.username), 'success')
            return redirect(next_url or url_for('admin.dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@auth.route('/logout/')
def logout():
    logout_user()
    flash('You have been signed out.', 'info')
    return redirect(url_for('main.index'))
