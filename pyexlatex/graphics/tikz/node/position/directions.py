from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.graphics.tikz.node.node import Node
from pyexlatex.models.item import ItemBase
from pyexlatex.models.package import Package
from pyexlatex.graphics.tikz.library import TikZLibrary


class DirectionBase(ItemBase):
    """
    Base class for relative positioning directions in TikZ, e.g. above, above right, etc.
    """

    name = '<invalid, do not use DirectionBase directly>'
    is_vertical_direction: Optional[bool] = None

    def __init__(self, direction: Optional['DirectionBase'] = None, of: Optional['Node'] = None,
                 by: Optional[float] = None, combined_direction: bool = True):
        """

        :param direction:
        :param of:
        :param by:
        :param combined_direction: In some usages of directions, they are specified together, e.g.
            above right=2cm and 3cm. In other usages, they are specified separately, e.g. above=2cm, right=3cm.
            When combined_direction=True, will use the former style, and when False will use the latter style
        """
        self.child_direction = direction
        self.of = of
        self.by = by
        self.combined_direction = combined_direction
        self._validate()
        self._set_vertical_and_horizontal_by()

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

        if self.has_combined_direction:
            return f'{vertical_name} {horizontal_name}{self.of_str}'

        # Handle non-combined direction

        return f'{vertical_name}{self.vertical_of_str}, {horizontal_name}{self.horizontal_of_str}'

    @property
    def has_combined_direction(self) -> bool:
        if self.child_direction is None:
            return self.combined_direction

        if not self.combined_direction or not self.child_direction.combined_direction:
            # Having False in either parent or child means entire is treated as False, since True is the default
            return False

        return True

    @property
    def of_str(self) -> str:
        if self.of is None and (self.child_direction is None or self.child_direction.of is None):
            if not self.by_str:
                return ''
            else:
                return f'={self.by_str}'

        return f'={self.by_str}of {self.of_label}'

    @property
    def vertical_of_str(self) -> Optional[str]:
        if self.has_combined_direction:
            return None

        if self.of is None and (self.child_direction is None or self.child_direction.of is None):
            if not self.vertical_by_str:
                return ''
            else:
                return f'={self.vertical_by_str}'

        return f'={self.vertical_by_str}of {self.of_label}'

    @property
    def horizontal_of_str(self) -> Optional[str]:
        if self.has_combined_direction:
            return None

        if self.of is None and (self.child_direction is None or self.child_direction.of is None):
            if not self.horizontal_by_str:
                return ''
            else:
                return f'={self.horizontal_by_str}'

        return f'={self.horizontal_by_str}of {self.of_label}'

    @property
    def of_label(self) -> Optional[str]:
        if self.of is None and (self.child_direction is None or self.child_direction.of is None):
            return None

        if self.of is not None:
            label = self.of.label
        elif self.child_direction is not None and self.child_direction.of is not None:
            label = self.child_direction.of.label
        else:
            return None

        return label


    @property
    def by_str(self) -> str:
        if self.by is None and (self.child_direction is None or self.child_direction.by is None):
            return ''

        out_str = ''
        if self.vertical_by_str is not None:
            out_str += self.vertical_by_str
        if self.horizontal_by_str is not None:
            out_str += self.horizontal_by_str

        return out_str

    @property
    def vertical_by_str(self) -> Optional[str]:
        if self.vertical_by is None:
            return None
        return f'{self.vertical_by}cm '

    @property
    def horizontal_by_str(self) -> Optional[str]:
        if self.horizontal_by is None:
            return None
        horizontal_str = f'{self.horizontal_by}cm '
        if self.has_combined_direction:
            horizontal_str = 'and ' + horizontal_str
        return horizontal_str

    def _set_vertical_and_horizontal_by(self):
        if self.by is None and (self.child_direction is None or self.child_direction.by is None):
            self.vertical_by = None
            self.horizontal_by = None
            return

        vertical_by, horizontal_by = None, None
        if _is_vertical_direction_and_has_by(self):
            vertical_by = self.by
        elif self.child_direction is not None and _is_vertical_direction_and_has_by(self.child_direction):
            vertical_by = self.child_direction.by

        if _is_horizontal_direction_and_has_by(self):
            horizontal_by = self.by
        elif self.child_direction is not None and _is_horizontal_direction_and_has_by(self.child_direction):
            horizontal_by = self.child_direction.by

        self.vertical_by = vertical_by
        self.horizontal_by = horizontal_by

    def __str__(self) -> str:
        return self.full_direction


class VerticalDirection(DirectionBase):
    is_vertical_direction = True


class HorizontalDirection(DirectionBase):
    is_vertical_direction = False


class Above(VerticalDirection):
    """
    Used for placing nodes: construct with one node, pass as placement to another node, that second node will
    be placed above the first node.
    """
    name = 'above'


class Right(HorizontalDirection):
    """
    Used for placing nodes: construct with one node, pass as placement to another node, that second node will
    be placed to the right of the first node.
    """
    name = 'right'


class Below(VerticalDirection):
    """
    Used for placing nodes: construct with one node, pass as placement to another node, that second node will
    be placed below the first node.
    """
    name = 'below'


class Left(HorizontalDirection):
    """
    Used for placing nodes: construct with one node, pass as placement to another node, that second node will
    be placed to the left of the first node.
    """
    name = 'left'


def _is_vertical_direction_and_has_by(direction: 'DirectionBase') -> bool:
    if direction.is_vertical_direction is None:
        return False
    return direction.is_vertical_direction and direction.by is not None


def _is_horizontal_direction_and_has_by(direction: 'DirectionBase') -> bool:
    if direction.is_vertical_direction is None:
        return False
    return not direction.is_vertical_direction and direction.by is not None
