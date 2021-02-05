from typing import Optional, Sequence
from copy import deepcopy

from pyexlatex.table.models.table.row import Row
from pyexlatex.logic.tools import _max_len_or_zero
from mixins.repr import ReprMixin


class TableSection(ReprMixin):
    repr_cols = ['rows']

    def __init__(self, rows: Sequence[Row], break_size_adjustment: Optional[str] = None):
        self.break_size_adjustment = break_size_adjustment
        self.rows = rows

    def __iter__(self):
        for row in self.rows:
            yield row

    def __getitem__(self, item):
        return self.rows[item]

    @property
    def length(self):
        return len(self.rows)

    @property
    def cell_width(self):
        return max([row.cell_width for row in self.rows])

    def __str__(self) -> str:
        from pyexlatex.table.logic.table.build import _build_tabular_str_from_rows_and_lines
        return _build_tabular_str_from_rows_and_lines(self.rows, self.break_size_adjustment)

    def __eq__(self, other):
        if not hasattr(other, 'rows'):
            return False
        if len(self.rows) != len(other.rows):
            return False

        for row, other_row in zip(self.rows, other.rows):
            if row != other_row:
                return False

        return True

    def __add__(self, other):
        # import here to avoid circular imports
        from pyexlatex.table.models.spacing.columntable import ColumnPadTable

        num_rows = max([self.length, other.length])

        out_rows = []

        for row_num in range(num_rows):
            out_row_class = _get_class_for_row(self, other, row_number=row_num)
            out_row = out_row_class([])
            try:
                out_row += self[row_num]
            except IndexError:
                # expected to hit here when sections have different numbers of rows
                out_row.pad(self.num_columns, direction='left')
            # Special handling for ColumnPadTable. Ignore rows, just always pad right
            if isinstance(other, ColumnPadTable):
                out_row.pad(self.num_columns + other.width, direction='right')
            else:
                try:
                    out_row += other[row_num]
                except IndexError:
                    out_row.pad(other.num_columns + self.num_columns, direction='right')

            out_rows.append(out_row)

        klass = self._add_class(other)

        return klass(out_rows)

    def __radd__(self, other):
        num_rows = max([self.length, other.length])

        out_rows = []

        for row_num in range(num_rows):
            out_row_class = _get_class_for_row(self, other, row_number=row_num)
            out_row = out_row_class([])
            try:
                out_row += other[row_num]
            except IndexError:
                out_row.pad(other.num_columns, direction='left')
            try:
                out_row += self[row_num]
            except IndexError:
                # expected to hit here when sections have different numbers of rows
                out_row.pad(self.num_columns + other.num_columns, direction='right')

            out_rows.append(out_row)

        klass = self._add_class(other)

        return klass(out_rows)

    def _add_class(self, other):
        # keep same class if both are same class
        # otherwise, default to Row class
        self_class = type(self)
        other_class = type(other)
        klass = self_class if self_class == other_class else TableSection

        # import here to avoid circular imports
        from pyexlatex.table.models.spacing.rowtable import RowPadTable
        from pyexlatex.table.models.spacing.columntable import ColumnPadTable
        if klass in (RowPadTable, ColumnPadTable):
            return TableSection

        return klass

    @property
    def num_columns(self):
        try:
            return self._num_columns
        except AttributeError:
            self._num_columns = self._set_num_columns()

        return self._num_columns

    def _set_num_columns(self):
        return _max_len_or_zero(self.rows)

    def join(self, sections):
        """
        Repliactes str.join behavior. Useful for creating padding spaces in a PanelGrid/PanelCollection
        :param sections:
        :return:
        """
        if len(sections) == 1:
            return sections[0]

        for i, section in enumerate(sections):
            if i == 0:
                out_section = deepcopy(section)
                continue
            else:
                out_section += self # insert self inbetween sections, replicating join behavior
            out_section = out_section + section

        return out_section

    def pad(self, length: int, direction='right'):
        """
        Expand table out to the right or left with blanks, until it is length passed (apply to every row)
        :param length:
        :param direction:
        :return:
        """
        [row.pad(length=length, direction=direction) for row in self.rows]

    @property
    def is_spacer(self):
        return all([row.is_spacer for row in self.rows])


    def _recreate_rows_if_created(self):
        """
        Used for recreating rows after labels or value table have been modified.
        Don't want to create rows if they've never been created before (initialization)
        :return:
        """
        # run creation process again
        if hasattr(self, '_rows'):
            self._rows = self._create_rows()
        # else, do nothing

    def _create_rows(self):
        raise NotImplementedError

def _get_class_for_row(*objs, row_number: int=0):
    from pyexlatex.table.models.texgen.lines import TableLineOfSegments
    from pyexlatex.table.models.labels.row import LabelRow, LabelCollection

    suggested_class = _get_by_row_number_first_class_without_index_error(*objs, row_number=row_number)

    # this is one row class that should not be created unless explicitly calling the rows method of LabelTable.
    # this is because LabelCollections contain underlines, which are created separately from LabelRows in the
    # _create_rows method of LabelTable. If adding a collection to a row, will lose the underline
    if issubclass(suggested_class, LabelRow):
        return LabelCollection

    # already got a row class, just return it
    if issubclass(suggested_class, (Row, TableLineOfSegments)):
        return suggested_class

    # otherwise, we have an item class. return the appropriate row class for that item
    return _get_row_class_for_item_class(suggested_class)


def _get_row_class_for_item_class(klass):
    from pyexlatex.table.models.texgen.lines import TableLineSegment, TableLineOfSegments
    from pyexlatex.table.models.data.dataitem import DataItem
    from pyexlatex.table.models.data.row import DataRow
    from pyexlatex.table.models.labels.label import Label
    from pyexlatex.table.models.labels.row import LabelRow, LabelCollection
    if issubclass(klass, TableLineSegment):
        return TableLineOfSegments
    if issubclass(klass, DataItem):
        return DataRow
    if issubclass(klass, (Label, LabelCollection)):
        return LabelCollection
    else:
        raise NotImplementedError(f'could not determine row class for item class {klass}')

def _get_by_row_number_first_class_without_index_error(*objs, row_number: int):
    attrs_or_none = _get_by_row_number_none_if_index_error(*objs, row_number=row_number)
    return _first_non_none_class(attrs_or_none)

def _get_by_row_number_none_if_index_error(*objs, row_number: int):
    out_attrs = []
    for obj in objs:
        try:
            out_attrs.append(obj[row_number])
        except IndexError:
            out_attrs.append(None)
    return out_attrs

def _first_non_none_class(objs):
    valid_objs = [obj for obj in objs if obj is not None]
    if len(valid_objs) == 0:
        raise ValueError('all objects passed were None. could not determine which class to use.')

    return type(valid_objs[0])
