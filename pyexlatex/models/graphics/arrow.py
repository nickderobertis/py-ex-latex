from typing import Sequence, Tuple, Optional, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay import Overlay
    from pyexlatex.models.graphics.tikz.node.node import Node
from pyexlatex.models.graphics.tikz.path import SpecificPath


class Arrow(SpecificPath):
    draw_type = '--'
    path_type = 'draw'

    def __init__(self, from_: Union[Tuple[int, int], 'Node'], to: Union[Tuple[int, int], 'Node'],
                 double_sided: bool = False,
                 options: Optional[Sequence[str]] = None,
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
