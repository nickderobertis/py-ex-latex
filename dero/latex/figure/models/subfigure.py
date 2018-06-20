

from dero.latex.figure.models.graphic import Graphic
from dero.latex.models import Item
from dero.latex.models.caption import Caption
from dero.latex.models.label import Label
from dero.latex.logic.builder import build_figure_content


class Subfigure(Item):
    """
    Used for more control over building figures
    """
    name = 'subfigure'

    def __init__(self, filepath, caption=None, label=None, centering=True, position_str=r'[t]{0.45\linewidth}'):
        self.graphic = Graphic(filepath)
        self.caption = Caption(caption) if caption else None
        self.label = Label(label) if label else None

        contents = build_figure_content(
            [self.graphic],
            caption=self.caption,
            label=self.label,
            centering=centering,
            position_str=position_str
        )

        super().__init__(self.name, contents)

    def __repr__(self):
        return f'<Subfigure({self.graphic.filepath}, caption={self.caption})>'



