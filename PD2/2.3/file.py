from functools import wraps
from collections import namedtuple


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
