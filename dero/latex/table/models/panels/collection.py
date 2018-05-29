from dero.latex.table.models.panels.panel import Panel
from dero.latex.models.mixins import ReprMixin

class PanelCollection(ReprMixin):
    repr_cols = ['panels']

    def __init__(self, panels: [Panel]):
        self.panels = panels