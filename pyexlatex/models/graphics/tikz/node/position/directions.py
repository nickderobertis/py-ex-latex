from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.models.graphics.tikz.node.node import Node
from pyexlatex.models.item import ItemBase
from pyexlatex.models.package import Package
from pyexlatex.models.graphics.tikz.library import TikZLibrary


class DirectionBase(ItemBase):
    """
    Base class for relative positioning directions in TikZ, e.g. above, above right, etc.
    """

    name = '<invalid, do not use DirectionBase directly>'
    is_vertical_direction = None

    def __init__(self, direction: Optional['DirectionBase'] = None, of: Optional['Node'] = None,
                 by: Optional[int] = None):
        self.child_direction = direction
        self.of = of
        self.by = by
        self._validate()

        self.init_data()
        self.data.packages.extend([
            Package('tikz'),
            TikZLibrary('positioning')
        ])

    def _validate(self):
        if self.child_direction is not None and self.of is not None:
            raise ValueError('must only pass of when there are no other child directions')
        if self.is_vertical_direction is None:
            raise ValueError('must set is_vertical_direction to True or False when subclassing DirectionBase')
        if self.child_direction is not None:
            if self.is_vertical_direction and self.child_direction.is_vertical_direction:
                raise ValueError('cannot combine vertical directions, must be a vertical and horizontal direction')
            if not self.is_vertical_direction and not self.child_direction.is_vertical_direction:
                raise ValueError('cannot combine horizontal directions, must be a vertical and horizontal direction')
            if self.of is not None and self.child_direction.of is not None:
                raise ValueError('cannot pass two of in nested directions')

    @property
    def full_direction(self) -> str:
        if self.child_direction is None:
            return f'{self.name}{self.of_str}'

        if self.is_vertical_direction:
            vertical_name = self.name
            horizontal_name = self.child_direction.name
        else:
            vertical_name = self.child_direction.name
            horizontal_name = self.name
        return f'{vertical_name} {horizontal_name}{self.of_str}'

    @property
    def of_str(self) -> str:
        if self.of is None and self.child_direction.of is None:
            return ''

        label = None
        if self.of is not None:
            label = self.of.label
        else:
            label = self.child_direction.of.label

        return f'={self.by_str}of {label}'

    @property
    def by_str(self) -> str:
        if self.by is None and (self.child_direction is None or self.child_direction.by is None):
            return ''

        vertical_by, horizontal_by = None, None
        if _is_vertical_direction_and_has_by(self):
            vertical_by = self.by
        elif self.child_direction is not None and _is_vertical_direction_and_has_by(self.child_direction):
            vertical_by = self.child_direction.by

        if _is_horizontal_direction_and_has_by(self):
            horizontal_by = self.by
        elif self.child_direction is not None and _is_horizontal_direction_and_has_by(self.child_direction):
            horizontal_by = self.child_direction.by

        out_str = ''
        if vertical_by is not None:
            out_str += f'{vertical_by} '
        if horizontal_by is not None:
            out_str += f'and {horizontal_by} '

        return out_str

    def __str__(self) -> str:
        return self.full_direction


class VerticalDirection(DirectionBase):
    is_vertical_direction = True


class HorizontalDirection(DirectionBase):
    is_vertical_direction = False


class Above(VerticalDirection):
    name = 'above'


class Right(HorizontalDirection):
    name = 'right'


class Below(VerticalDirection):
    name = 'below'


class Left(HorizontalDirection):
    name = 'left'


def _is_vertical_direction_and_has_by(direction: 'DirectionBase') -> bool:
    return direction.is_vertical_direction and direction.by is not None


def _is_horizontal_direction_and_has_by(direction: 'DirectionBase') -> bool:
    return not direction.is_vertical_direction and direction.by is not None