import re
from typing import Tuple

from pyexlatex.figure.models.graphic import Graphic
from pyexlatex.models.item import Item
from pyexlatex.models.caption import Caption
from pyexlatex.models.label import Label
from pyexlatex.logic.builder import build_figure_content
from pyexlatex.models.containeritem import ContainerItem

POSITION_STR_PATTERN = re.compile(r'\[([tcb])\]{([\d.\w\\]+)}')


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
        self.position_str = position_str
        self.anchor, self.width = anchor_and_width_from_position_str(self.position_str)

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


def anchor_and_width_from_position_str(position: str) -> Tuple[str, str]:
    if not isinstance(position, str):
        position = str(position)
    match = re.match(POSITION_STR_PATTERN, position)
    if not match:
        raise ValueError(f'could not parse position {position}')
    
    anchor = match.group(1)
    width = match.group(2)
    return anchor, width



