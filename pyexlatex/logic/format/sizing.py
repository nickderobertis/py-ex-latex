from typing import Any

from pyexlatex.models.format.centering import Center
from pyexlatex.models.format.adjustbox import AdjustBox
from pyexlatex.models.sizes.textheight import TextHeight
from pyexlatex.models.sizes.textwidth import TextWidth


def adjust_to_full_size_and_center(content: Any) -> Center:
    """
    Takes content and adjusts it to 90% text width, 80% text height, but keeping the aspect ratio.
    """

    content = adjust_to_size(content, 0.9, 0.8, keep_aspect_ratio=True)
    content = Center(content)
    return content


def adjust_to_size(content: Any, width: float, height: float, keep_aspect_ratio: bool = True
                   ) -> AdjustBox:
    adjust_options = [
        f'width={width}{TextWidth()}',
        f'height={height}{TextHeight()}',
    ]
    if keep_aspect_ratio:
        adjust_options.append('keepaspectratio')

    return AdjustBox(
        content,
        adjust_options=adjust_options
    )