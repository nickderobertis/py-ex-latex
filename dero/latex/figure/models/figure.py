
from dero.latex.figure.models.subfigure import Subfigure
from dero.latex.models import Item
from dero.latex.models.caption import Caption
from dero.latex.models.label import Label
from dero.latex.logic.builder import build_content

class Figure(Item):
    name = 'figure'

    def __init__(self, subfigures: [Subfigure], caption=None, label=None, centering=True, position_str=None):
        self.subfigures = subfigures
        self.caption = Caption(caption) if caption else None
        self.label = Label(label) if label else None

        content = build_content(
            self.subfigures,
            caption=self.caption,
            label=self.label,
            centering=centering,
            position_str=position_str
        )

        super().__init__(self.name, content)

    def __repr__(self):
        return f'<Figure(subfigures={self.subfigures}, caption={self.caption})>'