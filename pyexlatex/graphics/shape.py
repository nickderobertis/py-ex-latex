from typing import Sequence, Tuple, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay import Overlay
from pyexlatex.graphics.tikz.node.node import Node


class Shape(Node):
    shape_name = '<Do not use Shape directly, set shape_name in subclass>'

    def __init__(self, options: Optional[Sequence[str]] = None, offset: Tuple[int, int] = (0, 0), **kwargs):
        options = self._get_list_copy_from_list_or_none(options)
        options.extend([
            self.shape_name,
            'draw'
        ])
        super().__init__(options=options, location=offset, **kwargs)