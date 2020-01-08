from typing import Sequence, List, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.models.item import ItemBase
from pyexlatex.presentation.beamer.templates.frames.grid import GridFrame, Frame
from pyexlatex.figure.models.graphic import Graphic
from pyexlatex.models.format.fills import VFill
from pyexlatex.presentation.beamer.templates.frames.dim_reveal import DimRevealMixin
from pyexlatex.models.sizes.textheight import TextHeight
from pyexlatex.models.format.centering import Centering
from pyexlatex.layouts.multicol import MultiCol


class TwoColumnFrame(GridFrame):
    """
    Creates a GridFrame, automatically setting widths and heights as an even split based on the shape
    of the content passed
    """

    def __init__(self, left_content, right_content, **frame_kwargs):
        super().__init__([[left_content, right_content]], **frame_kwargs)


class BasicTwoColumnFrame(Frame):
    """
    Similar to TwoColumnFrame but does not put any constraints on vertical sizing
    """

    def __init__(self, left_content, right_content, **frame_kwargs):
        self.content = [left_content, right_content]
        self.layout = MultiCol(self.content)
        super().__init__(self.layout.content, **frame_kwargs)


class TwoGraphicBase:

    def __init__(self, content, graphics: Sequence, graphics_on_right: bool = True, **frame_kwargs):
        self.content = content
        self.graphics = graphics
        self.graphics_on_right = graphics_on_right
        super().__init__(self.left_content, self.right_content, **frame_kwargs)  # type: ignore

    @property
    def graphic_contents(self) -> List['ItemBase']:
        graphic_contents: List['ItemBase']
        graphic_contents = [Centering(), VFill()]
        for filepath_or_graphic in self.graphics:
            if isinstance(filepath_or_graphic, str):
                # Got filepath, need to make graphic
                graphic_contents.append(Graphic(
                    filepath_or_graphic,
                    width=0.9,
                    options=[
                        f'height={self.graphic_height}',
                        'keepaspectratio'
                    ]
                ))
            else:
                # Got a Graphic, TikZPicture, etc.
                graphic_contents.append(filepath_or_graphic)
            graphic_contents.append(VFill())
        graphic_contents.append(VFill())

        return graphic_contents

    @property
    def left_content(self):
        if self.graphics_on_right:
            return self.content
        else:
            return self.graphic_contents

    @property
    def right_content(self):
        if self.graphics_on_right:
            return self.graphic_contents
        else:
            return self.content

    @property
    def graphic_spacing(self) -> float:
        """
        Total amount of padding between images as a fraction of text height
        """
        return (len(self.graphics) - 1) * 0.20

    @property
    def graphic_height(self) -> str:
        total_area = 1 - self.graphic_spacing
        per_graphic = total_area / len(self.graphics)
        return f'{per_graphic}{TextHeight()}'


class TwoColumnGraphicFrame(TwoGraphicBase, TwoColumnFrame):
    """
    A GridFrame with graphics on one side and text on the other.
    """
    pass


class BasicTwoColumnGraphicFrame(TwoGraphicBase, BasicTwoColumnFrame):
    """
    Similar to TwoColumnGraphicFrame, but does not put any constraints on vertical sizing
    """
    pass


class TwoColumnGraphicDimRevealBase(DimRevealMixin):

    def __init__(self, content: Sequence[str], graphics: Sequence,
                 graphics_on_right: bool = True, ordered_list: bool = False,
                 **frame_kwargs):
        super().__init__(content, ordered_list=ordered_list,
                         graphics=graphics, graphics_on_right=graphics_on_right,
                         **frame_kwargs)


class TwoColumnGraphicDimRevealFrame(TwoColumnGraphicDimRevealBase, TwoColumnGraphicFrame):
    """
    A TwoColumnGraphicFrame where the non-graphic column is bulleted or numbered dim and reveal items
    """
    pass


class BasicTwoColumnGraphicDimRevealFrame(TwoColumnGraphicDimRevealBase, TwoColumnGraphicFrame):
    """
    A BasicTwoColumnGraphicFrame where the non-graphic column is bulleted or numbered dim and reveal items
    """
    pass