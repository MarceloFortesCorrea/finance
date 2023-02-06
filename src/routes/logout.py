# routes/logout.py

from flask import Blueprint, session, url_for, redirect


logout_bp = Blueprint('logout', __name__)


@logout_bp.route('/logout')
def logout():
    session.pop('login_in', None)
    return redirect(url_for('main.index'))
