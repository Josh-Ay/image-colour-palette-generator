from functools import wraps
from flask import abort, session


def login_required(function):
    @wraps(function)
    def wrapper_function(*args, **kwargs):
        if dict(session).get("user_profile") is not None:
            return function(*args, **kwargs)
        else:
            abort(status=403)

    return wrapper_function
