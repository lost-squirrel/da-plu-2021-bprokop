from functools import wraps


from functools import wraps
import types


def add_class_method(cls):
    def real_decorator(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            return(fn(*args, **kwargs))
        wrapper = types.MethodType(wrapper, cls)
        setattr(cls, fn.__name__, wrapper)
        return fn
    return real_decorator


def add_instance_method(cls):
    def real_decorator(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            return(fn(*args, **kwargs))
        setattr(cls, fn.__name__, wrapper)
        return fn
    return real_decorator
