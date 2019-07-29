import os
from typing import Union, List, Dict, Any, Optional
from copy import deepcopy
from dero.latex.models import Item
from dero.latex.models.section.base import TextAreaBase
from dero.latex.models.presentation.beamer.frame.title import FrameTitle


class Frame(TextAreaBase):
    name = 'frame'

    def __init__(self, content, title: Optional[str] = None, label: Optional[str] = None):
        self.title = title
        if isinstance(content, (Item, str)):
            content = [content]
        else:
            content = deepcopy(content)  # don't modify content inplace

        if self.title is not None:
            content.insert(0, FrameTitle(title))

        self.content = content
        # TODO: evaluate whether fragile can be passed for all frames and what the performance hit is. If cannot, then
        # TODO: must determine from contents whether fragile should be passed. Will require adding boolean data types
        # TODO: to item data
        super().__init__(self.name, self.content, label=label, env_modifiers='[fragile]')