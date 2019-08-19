from typing import Optional, Sequence, Any, List, Tuple
from dero.latex.models.presentation.beamer.frame.frame import Frame
from dero.latex.models.format.adjustbox import AdjustBox
from dero.latex.models.sizes.textwidth import TextWidth
from dero.latex.figure.models.graphic import Graphic
from dero.latex.models.format.vfill import VFill


class FullWidthFrame(Frame):
    """
    Resizes passed latex object to take up entire frame.
    """

    def __init__(self, content: Sequence[Sequence[Any]], **kwargs):
        content = adjust_to_full_width(content)
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
            cont = adjust_to_full_width(cont)
            all_content.extend([cont, VFill()])
        all_content = all_content[:-1]  # strip final VFill
        super().__init__(all_content, **kwargs)


def adjust_to_full_width(content: Any) -> AdjustBox:
    content = AdjustBox(
        content,
        adjust_options=[
            f'width={TextWidth()}'
        ]
    )
    return content
