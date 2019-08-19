from typing import Iterable


def _max_len_or_zero(iterable: Iterable) -> int:
    try:
        return max([len(i) for i in iterable])
    except ValueError:
        return 0


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


def _add_if_not_none(*items):
    not_none_items = [item for item in items if item is not None]

    if len(not_none_items) == 0:
        return None
    elif len(not_none_items) == 1:
        return not_none_items[0]

    return sum(not_none_items[1:], not_none_items[0])