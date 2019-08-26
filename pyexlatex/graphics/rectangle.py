from typing import Sequence, Tuple, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay import Overlay
from pyexlatex.graphics.tikz.path import SpecificPath


class Rectangle(SpecificPath):
    draw_type = 'rectangle'
    path_type = 'draw'

    def __init__(self, width: int, height: int, offset: Tuple[int, int] = (0, 0),
                 options: Optional[Sequence[str]] = None,
                 overlay: Optional['Overlay'] = None):
        self.size = (width, height)
        self.offset = offset
        super().__init__(self.get_points(), options=options, overlay=overlay)

    def get_points(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return (
            self.offset,
            (self.size[0] + self.offset[0], self.size[1] + self.offset[1])
        )