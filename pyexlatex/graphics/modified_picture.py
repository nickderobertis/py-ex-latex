from typing import Union, Sequence
from pyexlatex.models.template import Template
from pyexlatex.graphics.tikz.node.node import Node
from pyexlatex.graphics.tikz.scope import Scope
from pyexlatex.figure.models.graphic import Graphic
from pyexlatex.graphics.tikz.picture import TikZPicture
from pyexlatex.graphics.shape import Shape
from pyexlatex.graphics.tikz.item import TikZItem


class ModifiedPicture(Template):

    def __init__(self, picture: Union[str, Graphic, TikZPicture], draw_items: Sequence[Union[TikZItem, Shape]],
                 add_grid: bool = False):
        self.picture = picture
        self.draw_items = draw_items
        self.add_grid = add_grid
        self.contents = self._get_contents()
        super().__init__()

    def _get_graphic(self) -> Union[Graphic, TikZPicture]:
        if isinstance(self.picture, (TikZPicture, Graphic)):
            return self.picture

        # Assuming str of filepath was passed
        return Graphic(self.picture)

    def _get_contents(self):
        # Add the image as the contents of a node
        image_node = Node(self._get_graphic(), options=['anchor=south west'])

        if self.add_grid:
            # TODO [#4]: use models in drawing help lines grid
            draw_items = [
                r'\draw[help lines,xstep=.1,ystep=.1] (0,0) grid (1,1);',
                r'\foreach \x in {0,1,...,9} { \node [anchor=north] at (\x/10,0) {0.\x}; }',
                r'\foreach \y in {0,1,...,9} { \node [anchor=east] at (0,\y/10) {0.\y}; }',
                *self.draw_items
            ]
        else:
            draw_items = self.draw_items

        # Create a scope where the bounding box is the image node, now with a relative coordinate system (0, 1)
        scope = Scope(
            draw_items,
            options=[
                f'x={self._wrap_with_braces(f"({image_node.label}.south east)")}',
                f'y={self._wrap_with_braces(f"({image_node.label}.north west)")}'
            ]
        )

        picture = TikZPicture([
            image_node,
            scope
        ])

        return picture

