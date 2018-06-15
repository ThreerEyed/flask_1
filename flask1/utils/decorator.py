from flask import session, redirect, url_for
from functools import wraps


def is_login(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        user_session = session.get('user_id')
        if user_session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.user_login'))
    return check_login


def to_dict():
    pass