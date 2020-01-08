from typing import Sequence, List, Union
from pyexlatex.models.format.join import Joined


def join_with_commas_and_and(items: Sequence[str]) -> str:
    if len(items) == 0:
        return ''
    elif len(items) == 1:
        return items[0]
    elif len(items) == 2:
        # Use only and, not commas
        return f'{items[0]} and {items[1]}'

    # Length 3+, handled the same, commas for all and also and on the last join
    out_str = ', '.join(items[:-1])
    out_str += f', and {items[-1]}'
    return out_str


def join_with_commas_and_and_output_list(items: Sequence[str]) -> List[str]:
    if len(items) == 0:
        return ['']
    elif len(items) == 1:
        return [items[0]]
    elif len(items) == 2:
        # Use only and, not commas
        return [items[0], ' and ', items[1]]

    # Length 3+, handled the same, commas for all and also and on the last join
    out_list: List[Union[str, Joined]] = []
    for item in items[:-1]:
        out_list.append(Joined([item, ', ']))
    out_list[-1] = Joined([items[-2], ', and '])  # remove comma after last item added, replace with comma and and
    out_list.append(items[-1])

    return out_list
