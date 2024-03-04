from functools import wraps

from .connection import session_maker


def db_session(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        session_create = False
        if not hasattr(kwargs, "session"):
            session = session_maker()
            kwargs["session"] = session
            session_create = True
        else:
            session = None

        result = func(*args, **kwargs)

        if session_create:
            session.close()

        return result

    return wrapper
