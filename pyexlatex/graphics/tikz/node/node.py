import uuid
from typing import Tuple, Optional, Sequence, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay import Overlay

from pyexlatex.graphics.tikz.item import TikZItem
from pyexlatex.graphics.tikz.node.position.position import NodePosition
from pyexlatex.logic.format.contents import format_contents


class Node(TikZItem):

    def __init__(self, contents: Optional = None, location: Optional[Tuple[int, int]] = None,
                 label: Optional[str] = None,
                 options: Optional[Sequence[str]] = None,
                 overlay: Optional['Overlay'] = None):
        self.add_data_from_content(location)
        self.location = NodePosition(location)
        self.add_data_from_content(contents)
        self.content = format_contents(contents)
        self.label = label if label is not None else uuid.uuid4()

        options = self._get_list_copy_from_list_or_none(options)
        if self.location.relative_location:
            options.append(str(self.location))

        super().__init__(self.get_name(), self.content_str, options=options, overlay=overlay)

    def get_name(self) -> str:
        if self.content is None:
            return 'coordinate'
        else:
            return 'node'

    @property
    def absolute_location_str(self) -> str:
        if not self.location.absolute_location:
            return ''

        return str(self.location)


    @property
    def content_str(self) -> str:
        text = self._empty_str_if_none(self._wrap_with_braces(self.content))
        return f'({self.label}) {self.absolute_location_str} {text}'