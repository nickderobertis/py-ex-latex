from typing import Sequence, Tuple, Optional, List, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.graphics.shape import Shape


class Rectangle(Shape):
    """
    Draws a rectangle.
    """
    shape_name = 'rectangle'

    def __init__(self, width: int, height: int, contents: Optional[Any] = None,
                 offset: Tuple[int, int] = (0, 0), content_position: str = 'center',
                 content_offset: Optional[float] = None,
                 shape_options: Optional[List[str]] = None,
                 text_options: Optional[List[str]] = None,
                 overlay: Optional['Overlay'] = None, unit: str = 'cm'):
        self.size = (width, height)
        self.offset = offset
        self.unit = unit
        shape_options = self._get_list_copy_from_list_or_none(shape_options)
        shape_options.extend(self.get_size_options())

        super().__init__(
            contents=contents,
            content_position=content_position,
            content_offset=content_offset,
            shape_options=shape_options,
            text_options=text_options,
            overlay=overlay,
            offset=offset
        )

    def get_size_options(self) -> List[str]:
        return [
            f'minimum width={self.size[0]}{self.unit}',
            f'minimum height={self.size[1]}{self.unit}',
        ]