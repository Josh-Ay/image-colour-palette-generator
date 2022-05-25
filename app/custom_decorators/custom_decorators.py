from functools import wraps
from flask import abort, session
import os


def login_required(function):
    @wraps(function)
    def wrapper_function(*args, **kwargs):
        if dict(session).get("user_profile") is not None:
            return function(*args, **kwargs)
        else:
            abort(status=403)

    return wrapper_function


def admin_only(function):
    @wraps(function)
    def wrapper_function(*args, **kwargs):
        if dict(session).get("ADMIN_MAIL") is not None and dict(session).get("user_profile")["email"] == os.environ.get("ADMIN_MAIL"):
            return function(*args, **kwargs)
        else:
            abort(status=403)
    
    return wrapper_function