from copy import deepcopy

from dero.latex.table.models.table.row import Row


class TableSection:

    def __init__(self, rows: [Row]):
        self.rows = rows

    def __add__(self, other):
        num_rows = max([len(self.rows), len(other.rows)])

        out_rows = []

        for row_num in range(num_rows):
            out_row = Row()
            try:
                out_row += self[row_num]
            except IndexError:
                # expected to hit here when sections have different numbers of rows
                out_row.pad(self.num_columns, direction='left')
            try:
                out_row += other[row_num]
            except IndexError:
                out_row.pad(other.num_columns + self.num_columns, direction='right')

            out_rows.append(out_row)

        klass = self._add_class(other)

        return klass(out_rows)

    def __radd__(self, other):
        num_rows = max([len(self.rows), len(other.rows)])

        out_rows = []

        for row_num in range(num_rows):
            out_row = Row()
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

        return klass

    @property
    def num_columns(self):
        try:
            return self._num_columns
        except AttributeError:
            self._num_columns = self._set_num_columns()

        return self._num_columns

    def _set_num_columns(self):
        return max([len(row) for row in self.rows])

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

