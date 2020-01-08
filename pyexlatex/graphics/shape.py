from typing import Sequence, Tuple, Optional, Union, List, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.graphics.tikz.node.node import Node
from pyexlatex.models.item import ItemBase
from pyexlatex.graphics.tikz.node.position.directions import (
    Above,
    Below,
    Right,
    Left
)
from pyexlatex.models.section.base import TextAreaMixin


class Shape(TextAreaMixin, ItemBase):
    """
    Base class for creating individual shape classes, not intended to be used directly.
    """
    shape_name = '<Do not use Shape directly, set shape_name in subclass>'
    text_node: Optional[Node]

    def __init__(self, shape_options: Optional[List[str]] = None, text_options: Optional[List[str]] = None,
                 offset: Tuple[int, int] = (0, 0),
                 contents: Optional[Any] = None, content_position: str = 'center', content_offset: Optional[float] = None,
                 **kwargs):
        self.content_position = content_position.lower()
        self.content_offset = content_offset
        shape_options = self._get_list_copy_from_list_or_none(shape_options)
        text_options = self._get_list_copy_from_list_or_none(text_options)
        shape_options.extend([
            self.shape_name,
            'draw'
        ])
        self._validate()
        if self.content_position == 'center':
            # pass contents to shape node itself, as shape node is already at center
            shape_contents = contents
            shape_options.extend(text_options)
        else:
            shape_contents = None
        self.shape_node = Node(options=shape_options, location=offset, contents=shape_contents, **kwargs)

        if self.content_position != 'center' and contents is not None:
            # Need to create a second node for placing text other than in center
            text_options.append(self._get_text_placement())
            self.text_node = Node(
                options=text_options,
                location=self._get_text_node_location(),
                contents=contents
            )
        else:
            self.text_node = None

        ItemBase.__init__(self, **kwargs)

        contents = self._get_contents()
        self.add_data_from_content(contents)
        self.contents = self.format_contents(contents)

    def _validate(self):
        self._validate_position()
        self._validate_offset()

    def _validate_position(self):
        allowed_positions = (
            'center',
            'right',
            'left',
            'top',
            'bottom'
        )
        if self.content_position not in allowed_positions:
            raise ValueError(f'could not use content_position {self.content_position}, '
                             f'pass one of {", ".join(allowed_positions)}')

    def _validate_offset(self):
        if self.content_offset is not None and self.content_position == 'center':
            raise ValueError('cannot pass content_offset when content_position is center')

    def _get_text_placement(self) -> Union[Right, Left, Below, Above]:
        """
        Need to place the text beside the line, not on the line. E.g. placing on bottom, we want the text
        above the bottom line, not on the bottom line

        :return:
        """
        if self.content_position == 'right':
            return Left(by=self.content_offset, combined_direction=False)
        elif self.content_position == 'left':
            return Right(by=self.content_offset, combined_direction=False)
        elif self.content_position == 'top':
            return Below(by=self.content_offset, combined_direction=False)
        elif self.content_position == 'bottom':
            return Above(by=self.content_offset, combined_direction=False)
        else:
            raise ValueError(f'could not determine text placement from {self.content_position}')

    def _get_shape_anchor(self) -> str:
        """
        Side of the shape to anchor on for text
        """
        if self.content_position == 'right':
            return 'east'
        elif self.content_position == 'left':
            return 'west'
        elif self.content_position == 'top':
            return 'north'
        elif self.content_position == 'bottom':
            return 'south'
        else:
            raise ValueError(f'could not determine shape anchor from {self.content_position}')

    def _get_text_node_location(self) -> str:
        return f'{self.shape_node.label}.{self._get_shape_anchor()}'

    def _get_contents(self) -> List[Node]:
        possible_contents = [
            self.shape_node,
            self.text_node
        ]
        contents = [content for content in possible_contents if content is not None]
        return contents

    def __str__(self):
        if isinstance(self.contents, str):
            return self.contents
        from pyexlatex.logic.builder import _build
        return _build(self.contents)

    @property
    def label(self) -> Optional[str]:
        return self.shape_node.label
