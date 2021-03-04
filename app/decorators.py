from functools import wraps

from flask import g, request, redirect, url_for, flash


def login_required(f):
    """Decorator checking if the user is logged in."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user_token is None:
            flash('To access this page please sign in.')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function
