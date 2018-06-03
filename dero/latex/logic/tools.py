from typing import Iterable


def _max_len_or_zero(iterable: Iterable) -> int:
    try:
        return max([len(i) for i in iterable])
    except ValueError:
        return 0