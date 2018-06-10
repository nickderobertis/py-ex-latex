

from dero.latex.table.models.spacing.cell import CellSpacer
from dero.latex.table.models.data.row import DataRow
from dero.latex.table.models.data.valuestable import ValuesTable

class RowPadTable(ValuesTable):

    def __init__(self, num_cols: int = 1):
        row = DataRow([CellSpacer(num_cols)])
        super().__init__([row])

    @property
    def num_columns(self):
        return len(self.rows)

    def __repr__(self):
        return f'<RowPadTable({self.num_columns})>'



