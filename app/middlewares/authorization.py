from flask import session, redirect, flash, url_for, current_app


def has_scopes(scopes):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if all(scope in session.scopes for scope in scopes):
                return f(*args, **kwargs)
            else:
                flash('Unauthorized', 'danger')
                return redirect(url_for('index'))
    return decorator
