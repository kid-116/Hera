from functools import wraps

from flask import session, redirect, flash, url_for

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized', 'danger')
            return redirect(url_for('users.oauth2_authorize'))
    return wrap
