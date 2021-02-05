from typing import Union, Iterable, List
import re
from copy import deepcopy

from pyexlatex.logic.tools import _add_if_not_none
from pyexlatex.table.models.labels.label import Label
from pyexlatex.table.models.mixins.addvalues.row import RowAddMixin
from pyexlatex.table.models.table.rowbase import RowBase


class LabelCollection(RowBase):
    """
    Represents one row of labels. Use to construct a LabelTable to apply to a DataTable.

    Main usage is LabelCollection.from_str_list
    """
    repr_cols = ['values', 'underlines']

    def __init__(self, values: List[Label], underline: Union[int, str]=None):
        """

        :param values:
        :param underline: int, str, or None, pass index or label to underline, pass a str range, e.g. '2-5' for a
                          range of labels to underline, pass space separated indices as a str, e.g. '0 2' for
                          separated underlines, or a combination, e.g. '2-5 8'
        """
        if isinstance(values, tuple):
            values = list(values)
        self.values: List[Label] = values
        underline_label_indices = _convert_underline_to_label_index_list(underline)
        self.underlines = self._convert_label_indices_to_column_indices(underline_label_indices)

    def __str__(self):
        return str(sum(self.values))

    def matches(self, other):
        """
        Compare on the basis of having same values, rather than same instance
        Use regular equality to test if same instance
        :param other:
        :return:
        """
        for i, value in enumerate(self):
            try:
                other[i]
            except IndexError:
                return False # any one misalignment, no match
            if value != other[i]:
                return False

        # same number of rows, all rows equal
        return True

    @classmethod
    def from_str_list(cls, str_list: List[str], underline: Union[int, str]=None) -> 'LabelCollection':
        """

        Args:
            str_list:
            underline: int, str, or None, pass index or label to underline, pass a str range, e.g. '2-5' for a
                  range of labels to underline, pass space separated indices as a str, e.g. '0 2' for
                  separated underlines, or a combination, e.g. '2-5 8'

        Returns:

        """
        labels = [Label(value) for value in str_list]
        return cls(labels, underline=underline)

    @classmethod
    def parse_unknown_type(cls, unknown_type: Union[str, Iterable[str], 'LabelCollection']) -> 'LabelCollection':
        if isinstance(unknown_type, LabelCollection):
            return unknown_type
        if isinstance(unknown_type, str):
            unknown_type = [unknown_type]
        if isinstance(unknown_type, list):
            return LabelCollection.from_str_list(unknown_type)
        else:
            raise ValueError(f'unable to parse type {type(unknown_type)} into label collection')

    def _convert_label_indices_to_column_indices(self, label_indices: List[int]):
        column_indices: List[int] = []
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

    def shift_underlines(self, shift):
        if self.underlines is None:
            return
        self.underlines = [u + shift for u in self.underlines]

    def __add__(self, other):
        # need to handle shifting of indices
        if isinstance(other, LabelCollection):
            to_add = deepcopy(other)
            to_add.shift_underlines(len(self))
        else:
            to_add = other

        result = super().__add__(to_add)

        # carry through underlines with addition
        if isinstance(result, LabelCollection):
            underlines = _add_if_not_none(self.underlines, to_add.underlines)
            result.underlines = underlines

        return result

    def __radd__(self, other):
        # need to handle shifting of indices
        to_add = deepcopy(self)
        to_add.shift_underlines(len(self))

        result = RowAddMixin.radd(to_add, other)

        # carry through underlines with addition
        if isinstance(result, LabelCollection):
            if isinstance(other, LabelCollection):
                underlines = _add_if_not_none(to_add.underlines, other.underlines)
            else:
                underlines = to_add.underlines
            result.underlines = underlines

        return result

    def pad(self, length: int, direction='right'):
        """
        Expand row out to the right or left with blanks, until it is length passed
        :param length:
        :return:
        """

        # only necessary to move underline columns if padding left
        if direction == 'left':
            num_values_to_add = length - len(self)
            self.shift_underlines(num_values_to_add)

        super().pad(length=length, direction=direction)

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
    int_list: List[int] = []
    for part in underline.split():
        # handle each space separated part. if just a range, will only be one part
        # check if is range like '3-5'
        try:
            if _is_range_str(part):
                int_list += _range_str_to_int_list(part)
            else:
                int_list.append(int(part))
        except ValueError:
            raise NotImplementedError(f'could not parse underline str into int. full underline '
                                      f'str: {underline}. failed processing part: {part}')

    return int_list

def _range_str_to_int_list(underline: str):
    bottom, top = underline.split('-')
    return [i for i in range(int(bottom), int(top) + 1)]


def _is_range_str(underline: str):
    pattern = re.compile(r'\d+-\d+')
    if pattern.match(underline):
        return True
    else:
        return False
