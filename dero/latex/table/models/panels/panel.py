from dero.latex.table.models.panels.grid import PanelGrid, GridShape
from dero.latex.models.mixins import ReprMixin


class Panel(ReprMixin):
    repr_cols = ['panel_grid']

    def __init__(self, panel_grid: PanelGrid):
        self.panel_grid = panel_grid