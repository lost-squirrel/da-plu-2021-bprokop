from functools import wraps


def greetings(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        name = fn(*args, **kwargs)
        return 'Hello ' + " ".join(word.capitalize() for word in name.split())
    return inner
