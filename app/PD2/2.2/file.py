from functools import wraps


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
