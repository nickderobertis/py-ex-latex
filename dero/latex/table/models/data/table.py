from dero.latex.table.models.data.valuestable import ValuesTable
from dero.latex.table.models.table.section import TableSection
from dero.latex.table.models.labels.column import ColumnLabels
from dero.latex.table.models.labels.row import RowLabels


class DataTable(TableSection):

    def __init__(self, values_table: ValuesTable, column_labels: ColumnLabels=None, row_labels: RowLabels=None):
        self.values_table = values_table
        self.column_labels = column_labels
        self.row_labels = row_labels
        super().__init__()