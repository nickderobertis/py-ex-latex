

from dero.latex.table.models.data.dataitem import DataItem

class CellSpacer(DataItem):

    def __init__(self):
        super().__init__(' ')

    def __repr__(self):
        return '<CellSpacer>'