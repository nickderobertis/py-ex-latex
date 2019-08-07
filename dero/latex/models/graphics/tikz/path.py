from typing import Optional, Sequence, List, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from dero.latex.models.presentation.beamer.overlay.overlay import Overlay
    from dero.latex.models.graphics.tikz.node import Node
from dero.latex.models.graphics.tikz.item import TikZItem

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
    name = 'path'


    def __init__(self, path_type: str, points: Sequence[Tuple[float, float]],
                 draw_type: str = '--',
                 options: Optional[Sequence[str]] = None,
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
        locations: List[str] = []
        for location in self.points:
            if hasattr(location, 'is_Node') and location.is_Node:
                location: 'Node'
                locations.append(f'({location.label})')
            else:
                location: Tuple[float, float]
                locations.append(str(location))
        return self.draw_join_str.join(locations)
