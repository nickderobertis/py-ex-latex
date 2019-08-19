from typing import Sequence, List, Union
from pyexlatex.models.presentation.beamer.templates.frames.grid import AutoSizeGridFrame
from pyexlatex.figure.models.graphic import Graphic
from pyexlatex.models.format.vfill import VFill
from pyexlatex.models.presentation.beamer.templates.frames.dim_reveal import DimRevealMixin
from pyexlatex.models.sizes.textheight import TextHeight
from pyexlatex.models.format.centering import Centering


class TwoColumnFrame(AutoSizeGridFrame):

    def __init__(self, left_content, right_content, **frame_kwargs):
        super().__init__([[left_content, right_content]], **frame_kwargs)


class TwoColumnGraphicFrame(TwoColumnFrame):

    def __init__(self, content, graphic_filepaths: Sequence[str], graphics_on_right: bool = True, **frame_kwargs):
        self.content = content
        self.graphic_filepaths = graphic_filepaths
        self.graphics_on_right = graphics_on_right
        super().__init__(self.left_content, self.right_content, **frame_kwargs)

    @property
    def graphic_contents(self) -> List[Union[Graphic, VFill]]:
        graphic_contents = [Centering(), VFill()]
        for filepath in self.graphic_filepaths:
            graphic_contents.append(Graphic(
                filepath,
                width=0.9,
                options=[
                    f'height={self.graphic_height}',
                    'keepaspectratio'
                ]
            ))
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
        return (len(self.graphic_filepaths) - 1) * 0.20

    @property
    def graphic_height(self) -> str:
        total_area = 1 - self.graphic_spacing
        per_graphic = total_area/len(self.graphic_filepaths)
        return f'{per_graphic}{TextHeight()}'


class TwoColumnGraphicDimRevealFrame(DimRevealMixin, TwoColumnGraphicFrame):

    def __init__(self, content: Sequence[str], graphic_filepaths: Sequence[str],
                 graphics_on_right: bool = True, ordered_list: bool = False,
                 **frame_kwargs):
        super().__init__(content, ordered_list=ordered_list,
                         graphic_filepaths=graphic_filepaths, graphics_on_right=graphics_on_right,
                         **frame_kwargs)