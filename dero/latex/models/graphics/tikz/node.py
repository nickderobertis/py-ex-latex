from typing import Optional, Sequence, List, Tuple, TYPE_CHECKING
import uuid
if TYPE_CHECKING:
    from dero.latex.models.presentation.beamer.overlay.overlay import Overlay
from dero.latex.models.graphics.tikz.item import TikZItem


class Node(TikZItem):

    def __init__(self, location: Tuple[int, int], contents: Optional = None,
                 label: Optional[str] = None,
                 options: Optional[Sequence[str]] = None,
                 overlay: Optional['Overlay'] = None):
        self.location = location
        self.content = contents
        self.label = label if label is not None else uuid.uuid4()
        super().__init__(self.get_name(), self.content_str, options=options, overlay=overlay)

    def get_name(self) -> str:
        if self.content is None:
            return 'coordinate'
        else:
            return 'node'

    @property
    def location_str(self) -> str:
        return f'at {self.location}'

    @property
    def content_str(self) -> str:
        text = self._empty_str_if_none(self._wrap_with_braces(self.content))
        return f'({self.label}) {self.location_str} {text}'


