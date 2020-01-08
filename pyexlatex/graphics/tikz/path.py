from typing import Optional, Sequence, List, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay
    from pyexlatex.graphics.tikz.node.node import Node
    from pyexlatex.graphics.shape import Shape
from pyexlatex.graphics.tikz.item import TikZItem

PATH_TYPES = (
    'draw',
    'fill',
    'pattern',
    'shade',
    'clip',
    'use as bounding box'
)

Location = Union[Tuple[float, float], 'Node']


class Path(TikZItem):
    """
    Lower-level class for drawing individual lines or shapes, should only be needed to be used for very custom graphics
    """
    name = 'path'


    def __init__(self, path_type: str, points: Sequence[Union[Tuple[float, float], 'Node', 'Shape']],
                 draw_type: str = '--',
                 options: Optional[List[str]] = None,
                 overlay: Optional['Overlay'] = None):
        self.points = points
        self.draw_type = draw_type
        self.path_type = path_type.lower()
        self.options = options
        self._validate()

        super().__init__(self.name, self.path_str, options=self.all_options, overlay=overlay)


    def _validate(self):
        self._validate_path_type()

    def _validate_path_type(self):
        if self.path_type not in PATH_TYPES:
            raise ValueError(f'invalid path_type, got {self.path_type}, expected one of {", ".join(PATH_TYPES)}')

    @property
    def all_options(self) -> List[str]:
        options = [self.path_type]
        if self.options is not None:
            options.extend(self.options)
        return options

    @property
    def draw_join_str(self) -> str:
        return f' {self.draw_type} '

    @property
    def path_str(self) -> str:
        from pyexlatex.graphics.tikz.node.node import Node
        from pyexlatex.graphics.shape import Shape
        locations: List[str] = []
        for location in self.points:
            if isinstance(location, Node):
                locations.append(f'({location.label})')
            elif isinstance(location, Shape):
                locations.append(f'({location.shape_node.label})')
            else:
                # location: Tuple[float, float]
                locations.append(str(location))
        if len(locations) == 1:
            # Got a single point draw path, such as circle
            return f'{locations[0]} {self.draw_type}'
        return self.draw_join_str.join(locations)


class SpecificPath(Path):
    """
    Subclass this path to build specific paths such as rectangle, circle, arrow
    """
    draw_type = '<invalid, do not use SpecificPath directly>'
    path_type = '<invalid, do not use SpecificPath directly>'

    def __init__(self, points: Sequence[Tuple[float, float]], *args, **kwargs):
        super().__init__(self.path_type, points, draw_type=self.draw_type, **kwargs)
