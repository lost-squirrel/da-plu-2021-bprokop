import types
from collections import namedtuple
from functools import wraps


def greetings(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        name = fn(*args, **kwargs)
        return 'Hello ' + " ".join(word.capitalize() for word in name.split())
    return inner


def is_palindrome(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        sentence = fn(*args, **kwargs)
        filtered_sentence = ''.join(filter(str.isalnum, str.upper(sentence)))
        if filtered_sentence == filtered_sentence[::-1]:
            return sentence + ' - is palindrome'
        else:
            return sentence + ' - is not palindrome'
    return inner


def format_output(*args):
    def real_decorator(fn):
        @wraps(fn)
        def wrapper(*wrapper_args, **kwargs):
            Argument = namedtuple('Argument', ['original', 'split'])
            arguments = [Argument(arg, str.split(arg, sep='__'))
                         for arg in args]
            fn_dict = fn(*wrapper_args, **kwargs)
            result_dict = {}
            validated_arguments = [
                arg in fn_dict for seq in arguments for arg in seq.split]
            if not all(validated_arguments):
                raise ValueError
            for argument in arguments:
                result_dict[argument.original] = " ".join(
                    [fn_dict[x] for x in argument.split])
            return result_dict
        return wrapper
    return real_decorator


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
