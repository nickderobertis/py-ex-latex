

from pyexlatex.figure.models.graphic import Graphic
from pyexlatex.models import Item
from pyexlatex.models.caption import Caption
from pyexlatex.models.label import Label
from pyexlatex.logic.builder import build_figure_content
from pyexlatex.models.containeritem import ContainerItem


class Subfigure(ContainerItem, Item):
    """
    Used for more control over building figures
    """
    name = 'subfigure'

    def __init__(self, filepath, caption=None, label=None, centering=True, position_str=r'[t]{0.45\linewidth}',
                 cache: bool = True):
        self.graphic = Graphic(filepath, cache=cache)
        self.caption = Caption(caption) if caption else None
        self.label = Label(label) if label else None

        self.add_data_from_content(self.graphic)

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



