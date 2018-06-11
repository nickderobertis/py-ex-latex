from dero.latex.models.mixins import ReprMixin
from dero.latex.table.models.panels.collection import PanelCollection
from dero.latex.table.models.table.caption import Caption



class Table(ReprMixin):
    repr_cols = ['caption', 'above_text', 'panels', 'below_text']

    def __init__(self, panels: PanelCollection, caption: Caption, above_text: str=None, below_text: str=None):
        self.panels = panels
        self.caption = caption
        self.above_text = above_text
        self.below_text = below_text