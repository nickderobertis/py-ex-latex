from typing import Tuple, Union, Optional
from pyexlatex.models.graphics.tikz.node.position.directions import DirectionBase


class NodePosition:

    def __init__(self, location: Optional[Union[Tuple[int, int], DirectionBase]] = None):
        self.location = location
        self.absolute_location, self.relative_location = False, False
        if location is not None:
            if isinstance(location, (tuple, list)):
                self.absolute_location = True
            else:
                self.relative_location = True

    def __str__(self) -> str:
        if self.location is None:
            return ''

        if self.absolute_location:
            return f'at {self.location}'

        if self.relative_location:
            return str(self.location)