

from dero.latex.table.models.spacing.cell import CellSpacer
from dero.latex.table.models.data.row import DataRow
from dero.latex.table.models.data.valuestable import ValuesTable

class ColumnPadTable(ValuesTable):

    def __init__(self, num_rows: int = 1):
        rows = ColumnPadTable._create_data_rows(num_rows)
        super().__init__(rows)

    @staticmethod
    def _create_data_rows(num_rows: int):
        return [DataRow([CellSpacer()]) for i in range(num_rows)]

    @property
    def num_columns(self):
        return 1

    def __repr__(self):
        return f'<ColumnPadTable({len(self.rows)})>'



