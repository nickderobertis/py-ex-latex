from typing import Sequence, Tuple, Optional, List, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay import Overlay
from pyexlatex.graphics.shape import Shape


class Rectangle(Shape):
    """
    Draws a rectangle.
    """
    shape_name = 'rectangle'

    def __init__(self, width: int, height: int, contents: Optional = None,
                 offset: Tuple[int, int] = (0, 0), content_position: str = 'center',
                 options: Optional[Sequence[str]] = None,
                 overlay: Optional['Overlay'] = None):
        self.size = (width, height)
        self.offset = offset
        options = self._get_list_copy_from_list_or_none(options)
        options.extend(self.get_size_options())

        super().__init__(
            contents=contents,
            content_position=content_position,
            options=options,
            overlay=overlay,
            offset=offset
        )

    def get_size_options(self) -> List[str]:
        return [
            f'minimum width={self.size[0]}cm',
            f'minimum height={self.size[1]}cm',
        ]