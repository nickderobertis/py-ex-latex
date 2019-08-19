from typing import Union, AnyStr


def _set_top_left_corner_labels(top_left_corner_labels = None):
    from pyexlatex.table import LabelTable, LabelCollection

    if top_left_corner_labels is None:
        return LabelTable.from_list_of_lists([[' ']])

    if isinstance(top_left_corner_labels, LabelTable):
        return top_left_corner_labels
    elif isinstance(top_left_corner_labels, LabelCollection):
        return LabelTable([top_left_corner_labels])
    elif isinstance(top_left_corner_labels, list):
        return LabelTable.from_list_of_lists([top_left_corner_labels]).T
    elif isinstance(top_left_corner_labels, str):
        return LabelTable.from_list_of_lists([[top_left_corner_labels]])
    else:
        raise NotImplementedError(f'was not able to create LabelTable out of {top_left_corner_labels}')