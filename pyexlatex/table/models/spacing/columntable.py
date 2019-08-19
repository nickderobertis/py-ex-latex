from copy import deepcopy

from pyexlatex.table.models.spacing.cell import CellSpacer
from pyexlatex.table.models.table.section import TableSection
from pyexlatex.table.models.data.valuestable import ValuesTable

class ColumnPadTable(ValuesTable):

    def __init__(self, width: int=1):
        self.width = width
        super().__init__([])

    @property
    def num_columns(self):
        return 1

    def __repr__(self):
        return f'<ColumnPadTable({len(self.rows)})>'

    def __add__(self, other):

        if not isinstance(other, TableSection):
            raise NotImplementedError

        out_section: TableSection = deepcopy(other)

        for row in out_section.rows:
            row.pad(other.num_columns + self.width, direction='left')

        return out_section



