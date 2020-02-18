from copy import deepcopy
from typing import List

from pyexlatex.texgen import _toprule_str, _midrule_str, _bottomrule_str, _cmidrule_str
from pyexlatex.models.mixins import StringAdditionMixin
from mixins.repr import ReprMixin
from pyexlatex.table.models.mixins.addvalues.row import RowAddMixin


class TableLine(StringAdditionMixin, ReprMixin):
        pass

class TopRule(TableLine):
    """
    A line which can be added on the top of a table
    """

    def __str__(self):
        return _toprule_str()


class MidRule(TableLine):
    """
    A line which can be added in the middle of a table
    """

    def __str__(self):
        return _midrule_str()

class BottomRule(TableLine):
    """
    A line which can be added at the bottom of a table
    """

    def __str__(self):
        return _bottomrule_str()

class TableLineSegment(StringAdditionMixin, ReprMixin, RowAddMixin):
    """
    A table line which does not need to stretch to the full length of the table
    """
    repr_cols = ['col_from', 'col_to']

    def __init__(self, col_from: int, col_to: int=None, align: str='lr'):
        self.col_from = col_from
        self.col_to = col_to
        self.align = align

    def __str__(self):
        return _cmidrule_str(self.align, self._range_str)

    def __len__(self):
        if self.col_to is None:
            return 1

        return (self.col_to - self.col_from) + 1

    def shift(self, shift: int):
        """
        Increments col_from and col_to by int. Used to shift underlines as tables are combined
        :return:
        """
        self.col_from += shift
        if self.col_to is not None:
            self.col_to += shift

    @property
    def _range_str(self):
        # add 1 to all columns to reindex to latex indices (1-based) from python indices (0-based)

        if self.col_to is None:
            col_to = self.col_from # single column
        else:
            col_to = self.col_to # multi column

        return f'{self.col_from + 1}-{col_to + 1}'


    def _add_class(self, other):
        return TableLineOfSegments

    @classmethod
    def from_list_of_ints(cls, int_list: List[int]):
        if len(int_list) == 1:
            return cls(int_list[0])
        else:
            return cls(int_list[0], int_list[-1])

    @property
    def is_spacer(self):
        return True

class TableLineOfSegments(RowAddMixin, TableLine):
    repr_cols = ['values', 'num_columns']

    def __init__(self, segments: List[TableLineSegment], num_columns: int=None):
        self.values = segments
        self.num_columns = num_columns

    def __str__(self):
        return ' '.join(str(segment) for segment in self.values)

    def __len__(self):
        return self.num_columns

    def __add__(self, other):
        # need to handle shifting of indices
        if isinstance(other, (TableLineOfSegments, TableLineSegment)):
            to_add = deepcopy(other)
            to_add.shift(len(self))
        else:
            raise NotImplementedError(f'cannot add type {type(other)} to TableLineOfSegments')
        line_of_segments: TableLineOfSegments =  super().__add__(to_add)
        line_of_segments.num_columns = self.num_columns + to_add.num_columns
        return line_of_segments

    def __radd__(self, other):
        # need to handle shifting of indices
        try:
            shift = len(other)
        except TypeError:
            raise NotImplementedError('cannot right add TableLineOfSegments without knowing how many columns to shift. '
                                      f'Could not calculate length of other. type of other: {type(other)}')
        to_add = deepcopy(self)
        to_add.shift(shift)
        line_of_segments: TableLineOfSegments = RowAddMixin.radd(to_add, other)
        line_of_segments.num_columns = self.num_columns + other.num_columns
        return line_of_segments

    def __getitem__(self, item):
        return self.values[item]

    def __iter__(self):
        for value in self.values:
            yield value

    @property
    def num_columns(self):
        return self._num_columns

    @num_columns.setter
    def num_columns(self, num_columns):
        if num_columns is None:
            self._num_columns = 0
        elif isinstance(num_columns, int):
            self._num_columns = num_columns
        else:
            raise ValueError(f'must provide int or None for num columns in TableLineOfSegments. got {num_columns}')

    def shift(self, shift):
        """
        Increments col_from and col_to by int for all segments within this line of segments
        :param shift:
        :return:
        """
        #### TEMP
        # import pdb
        # pdb.set_trace()
        #### END TEMP
        [value.shift(shift) for value in self.values]

    def _add_class(self, other):
        return TableLineOfSegments

    @classmethod
    def from_list_of_ints(cls, int_list: List[int], num_columns: int=None):
        if len(int_list) == 1:
            return cls([TableLineSegment(int_list[0])])

        # create ranges out of consecutive ints. Add segments with either ranges or individual ints
        segments = []
        current_range = []
        last_int: int = 0
        for i, int_ in enumerate(int_list):
            if i != 0:
                # now have int and last int for all loops
                if int_ - last_int == 1:  # consecutive range continues
                    current_range.append(int_)
                else:  # break in range. need to output prior, and start new range
                    segments.append(TableLineSegment.from_list_of_ints(current_range))
                    current_range = [int_]

            last_int = int_
            if i == 0: # initialization
                current_range.append(int_)

        segments.append(TableLineSegment.from_list_of_ints(current_range))

        return cls(segments, num_columns=num_columns)

    def pad(self, length: int, direction='right'):
        """
        Method is here to avoid errors when adding rows together through TableSection.__add__
        No padding is actually necessary for these rows as they are not in the tabular format,
        these lines only specify the columns which need to be underlined.

        However when padding left, we just need to shift the values rather than creating padding
        """
        direction = direction.lower().strip()
        if direction == 'right':
            pass # no shift necessary, column numbers have not changed
        elif direction == 'left':
            self.shift(length - len(self)) # shift column indices right to adjust for new left cells
        else:
            raise ValueError(f'must pass right or left for direction. got {direction}')

        self.num_columns = length # extend number of columns to new length

    @property
    def is_spacer(self):
        return all([value.is_spacer for value in self.values])