from typing import Optional
from copy import deepcopy
from pyexlatex.models.item import Item
from pyexlatex.models.section.base import TextAreaBase
from pyexlatex.presentation.beamer.frame.title import FrameTitle
from pyexlatex.constants.flags import HAS_MINTED


class Frame(TextAreaBase):
    """
    Basic unit for creating a slide in a presentation.
    """
    name = 'frame'

    def __init__(self, content, title: Optional[str] = None, label: Optional[str] = None, **kwargs):
        self.title = title
        if isinstance(content, (Item, str)):
            content = [content]
        else:
            content = deepcopy(content)  # don't modify content inplace

        if self.title is not None:
            content.insert(0, FrameTitle(self.title))

        self.add_data_from_content(content)

        self.content = content
        super().__init__(self.name, self.content, label=label, env_modifiers=self._get_env_modifiers(), **kwargs)

    @property
    def is_fragile(self) -> bool:
        if HAS_MINTED in self.data.flags:
            # Minted package requires using fragile frames
            return True

        return False

    def _get_env_modifiers(self) -> str:
        modifiers = []
        if self.is_fragile:
            modifiers.append('fragile')
        # Add any other fragile conditions here

        if not modifiers:
            return ''

        modifiers_str = ', '.join(modifiers)
        return self._wrap_with_bracket(modifiers_str)
