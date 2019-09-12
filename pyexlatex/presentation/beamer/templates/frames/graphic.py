from typing import Sequence, Any, Union

from pyexlatex.logic.format.sizing import adjust_to_full_size_and_center, adjust_to_size
from pyexlatex.presentation.beamer.frame.frame import Frame
from pyexlatex.figure.models.graphic import Graphic
from pyexlatex.models.format.fills import VFill, HFill
from pyexlatex.models.format.centering import Center


class FullWidthFrame(Frame):
    """
    Resizes passed latex object to take up entire frame.
    """

    def __init__(self, content: Sequence[Sequence[Any]], **kwargs):
        content = adjust_to_full_size_and_center(content)
        super().__init__(content, **kwargs)


class GraphicFrame(FullWidthFrame):
    """
    Resizes passed graphic to take up entire frame. Can pass a file path or a latex object.
    """

    def __init__(self, content: Any, **kwargs):
        if isinstance(content, str):
            content = Graphic(content)
        super().__init__(content, **kwargs)


class MultiGraphicFrame(Frame):
    """
    Resizes each graphic to full width and puts vertical space in between graphics.
    Can pass a file path or a latex object.
    """
    HORIZTONAL_SPACING = 0.05
    VERTICAL_SPACING = 0.05
    MAX_WIDTH = 0.9
    MAX_HEIGHT = 0.8

    def __init__(self, content: Sequence[Sequence[Any]], vertical: bool = True, **kwargs):
        self.vertical = vertical
        self.num_contents = len(content)
        all_content = []
        for cont in content:
            if isinstance(cont, str):
                cont = Graphic(cont)
            cont = adjust_to_size(cont, width=self._graphic_width, height=self._graphic_height)
            if self.vertical:
                cont = Center(cont)
            all_content.extend([cont, self._spacer_obj])
        all_content = all_content[:-1]  # strip final spacer
        super().__init__(all_content, **kwargs)

    @property
    def _graphic_width(self) -> float:
        if self.vertical:
            return self.MAX_WIDTH

        num_spacers = self.num_contents - 1
        spacer_space = self.HORIZTONAL_SPACING * num_spacers
        available_space = self.MAX_WIDTH - spacer_space
        space_per_graphic = available_space / self.num_contents

        return space_per_graphic

    @property
    def _graphic_height(self) -> float:
        if not self.vertical:
            return self.MAX_HEIGHT

        num_spacers = self.num_contents - 1
        spacer_space = self.VERTICAL_SPACING * num_spacers
        available_space = self.MAX_HEIGHT - spacer_space
        space_per_graphic = available_space / self.num_contents

        return space_per_graphic

    @property
    def _spacer_obj(self) -> Union[VFill, HFill]:
        if self.vertical:
            return VFill()

        return HFill()




