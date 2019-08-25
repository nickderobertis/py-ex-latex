from typing import Optional
from copy import deepcopy
from pyexlatex.models import Item
from pyexlatex.models.section.base import TextAreaBase
from pyexlatex.presentation.beamer import FrameTitle


class Frame(TextAreaBase):
    name = 'frame'

    def __init__(self, content, title: Optional[str] = None, label: Optional[str] = None, **kwargs):
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
        super().__init__(self.name, self.content, label=label, env_modifiers='[fragile]', **kwargs)