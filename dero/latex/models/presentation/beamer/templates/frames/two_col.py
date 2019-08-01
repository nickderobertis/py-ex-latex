from typing import Sequence, List, Union
from dero.latex.models.presentation.beamer.templates.frames.grid import AutoSizeGridFrame
from dero.latex.figure.models.graphic import Graphic
from dero.latex.models.format.vfill import VFill
from dero.latex.models.presentation.beamer.templates.lists.dim_reveal_items import DimAndRevealListItems
from dero.latex.models.presentation.beamer.templates.frames.dim_reveal import DimRevealMixin
from dero.latex.models.lists.ordered import OrderedList
from dero.latex.models.lists.unordered import UnorderedList


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
        graphic_contents = [VFill()]
        for filepath in self.graphic_filepaths:
            graphic_contents.append(Graphic(filepath))
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


class TwoColumnGraphicDimRevealFrame(DimRevealMixin, TwoColumnGraphicFrame):

    def __init__(self, content: Sequence[str], graphic_filepaths: Sequence[str],
                 graphics_on_right: bool = True, ordered_list: bool = False,
                 **frame_kwargs):
        super().__init__(content, ordered_list=ordered_list,
                         graphic_filepaths=graphic_filepaths, graphics_on_right=graphics_on_right,
                         **frame_kwargs)