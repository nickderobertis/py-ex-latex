from typing import Sequence, Any
from pyexlatex.presentation.beamer.frame.frame import Frame
from pyexlatex.models.format.adjustbox import AdjustBox
from pyexlatex.models.sizes.textwidth import TextWidth
from pyexlatex.models.sizes.textheight import TextHeight
from pyexlatex.figure.models.graphic import Graphic
from pyexlatex.models.format.vfill import VFill
from pyexlatex.models.format.centering import Center


class FullWidthFrame(Frame):
    """
    Resizes passed latex object to take up entire frame.
    """

    def __init__(self, content: Sequence[Sequence[Any]], **kwargs):
        content = adjust_to_full_size(content)
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

    def __init__(self, content: Sequence[Sequence[Any]], **kwargs):
        all_content = []
        for cont in content:
            if isinstance(content, str):
                cont = Graphic(cont)
            cont = adjust_to_full_size(cont)
            all_content.extend([cont, VFill()])
        all_content = all_content[:-1]  # strip final VFill
        super().__init__(all_content, **kwargs)


def adjust_to_full_size(content: Any) -> Center:
    content = AdjustBox(
        content,
        adjust_options=[
            f'width=0.9{TextWidth()}',
            f'height=0.8{TextHeight()}',
            'keepaspectratio'

        ]
    )
    content = Center(content)
    return content
