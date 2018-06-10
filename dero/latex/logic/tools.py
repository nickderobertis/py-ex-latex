from typing import Iterable


def _max_len_or_zero(iterable: Iterable) -> int:
    try:
        return max([len(i) for i in iterable])
    except ValueError:
        return 0

def show_contents(obj):
    print(_readable_repr(repr(obj)))

def _readable_repr(repr_str):
    out_letters = []
    num_tabs = 1
    for letter in repr_str:
        if letter in (')',']'):
            num_tabs -= 1
            out_letters += ['\n'] + ['   '] * num_tabs
        out_letters.append(letter)
        if letter in ('(','['):
            out_letters += ['\n'] + ['   '] * num_tabs
            num_tabs += 1
    return ''.join(out_letters)