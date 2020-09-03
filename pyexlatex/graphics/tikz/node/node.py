import random
import uuid
from typing import Tuple, Optional, Union, TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay

from pyexlatex.graphics.tikz.item import TikZItem
from pyexlatex.graphics.tikz.node.position.position import NodePosition
from pyexlatex.logic.format.contents import format_contents
from pyexlatex.graphics.tikz.node.position.directions import DirectionBase


class Node(TikZItem):
    """
    Represents a location in a graphic, but can also have a style and text, e.g. rectangle filled with text
    """
    label: Optional[str]

    def __init__(self, contents: Optional[Any] = None, location: Optional[Union[Tuple[int, int], DirectionBase, str]] = None,
                 label: Optional[str] = None,
                 options: Optional[List[str]] = None,
                 overlay: Optional['Overlay'] = None):
        self.add_data_from_content(location)
        self.location = NodePosition(location)
        self.add_data_from_content(contents)
        self.content = format_contents(contents)
        self.label = label if label is not None else str(random_uuid())

        options = self._get_list_copy_from_list_or_none(options)
        if self.location.relative_location:
            options.append(str(self.location))

        super().__init__(self.get_name(), self.content, options=options, overlay=overlay)

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

    def __str__(self):
        overlay = self.overlay if self.overlay is not None else ""
        item_str = fr'\{self.name}{overlay} {self.options_str} {self.content_str};'
        return item_str


def random_uuid():
    return uuid.UUID(bytes=bytes(random.getrandbits(8) for _ in range(16)), version=4)
