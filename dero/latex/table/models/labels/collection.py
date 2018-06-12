from typing import Union
import re

from dero.latex.table.models.labels.label import Label
from dero.latex.models.mixins import ReprMixin
from dero.latex.table.models.mixins.addvalues.row import RowAddMixin


class LabelCollection(RowAddMixin, ReprMixin):
    repr_cols = ['values', 'underlines']

    def __init__(self, values: [Label], underline: Union[int, str]=None):
        """

        :param values:
        :param underline: int, str, or None, pass index or label to underline, pass a str range, e.g. '2-5' for a
                          range of labels to underline, pass space separated indices as a str, e.g. '0 2' for
                          separated underlines, or a combination, e.g. '2-5 8'
        """
        if isinstance(values, tuple):
            values = list(values)
        self.values = values
        underline_label_indices = _convert_underline_to_label_index_list(underline)
        self.underlines = self._convert_label_indices_to_column_indices(underline_label_indices)

    def __iter__(self):
        for label in self.values:
            yield label

    def __getitem__(self, item):
        return self.values[item]

    def __str__(self):
        return str(sum(self.values))

    def __len__(self):
        return sum(_get_item_length(value) for value in self.values)

    def matches(self, other):
        """
        Compare on the basis of having same values, rather than same instance
        Use regular equality to test if same instance
        :param other:
        :return:
        """
        matches = [value == other[i] for i, value in enumerate(self)]
        return all(matches)

    @classmethod
    def from_str_list(cls, str_list):
        labels = [Label(value) for value in str_list]
        return cls(labels)

    def _convert_label_indices_to_column_indices(self, label_indices: [int]):
        column_indices = []
        position = 0
        for i, value in enumerate(self.values):
            begin_position = position
            position += _get_item_length(value)
            # if this label is included in label indices, add all ints in the range of span of label
            if i in label_indices:
                column_indices += [i for i in range(begin_position, position)]

        if column_indices == []:
            return None

        return column_indices


def _get_item_length(item):
    if isinstance(item, Label):
        return len(item)
    else:
        return 1

def _convert_underline_to_label_index_list(underline: Union[int, str]=None):
    if underline is None:
        return []

    assert isinstance(underline, (int, str))

    if isinstance(underline, int):
        return [underline]

    # underline is str
    int_list = []
    for part in underline.split():
        # handle each space separated part. if just a range, will only be one part
        # check if is range like '3-5'
        if _is_range_str(part):
            int_list += _range_str_to_int_list(part)
        try:
            int_list.append(int(part))
        except ValueError:
            raise NotImplementedError(f'could not parse underline str into int. full underline '
                                      f'str: {underline}. failed processing part: {part}')

    return int_list

def _range_str_to_int_list(underline: str):
    bottom, top = underline.split('-')
    return [i for i in range(bottom, top + 1)]


def _is_range_str(underline: str):
    pattern = re.compile(r'\d+-\d+')
    if pattern.match(underline):
        return True
    else:
        return False
