from typing import Sequence, Tuple, Optional, Union, TYPE_CHECKING, List

if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay
    from pyexlatex.graphics.tikz.node.node import Node
from pyexlatex.graphics.tikz.path import SpecificPath


class Arrow(SpecificPath):
    """
    Draws an arrow from one location to another.
    """
    draw_type = '--'
    path_type = 'draw'

    def __init__(self, from_: Union[Tuple[int, int], 'Node'], to: Union[Tuple[int, int], 'Node'],
                 double_sided: bool = False,
                 options: Optional[List[str]] = None,
                 overlay: Optional['Overlay'] = None):
        self.from_ = from_
        self.to = to
        self.double_sided = double_sided

        options = self._get_list_copy_from_list_or_none(options)
        options.append(self.arrow_option)

        super().__init__((from_, to), options=options, overlay=overlay)

    @property
    def arrow_option(self) -> str:
        if self.double_sided:
            return '<->'
        return '->'
