from typing import Optional
from dero.latex.models.item import Item
from dero.mixins.repr import ReprMixin


class SectionBase(Item, ReprMixin):
    name = 'section'
    repr_cols = ['title', 'short_title', 'contents']

    def __init__(self, contents, title: str, short_title: Optional[str] = None):
        self.title = title
        self.short_title = short_title
        super().__init__(self.name, contents, env_modifiers=self.env_modifiers)

    @property
    def env_modifiers(self):
        modifier_str = ''
        if self.short_title is not None:
            modifier_str += f'[{self.short_title}]'

        modifier_str += f'{{{self.title}}}'

        return modifier_str


class ParagraphBase(Item, ReprMixin):
    name = 'paragraph'
    repr_cols = ['title', 'contents']

    def __init__(self, contents, title: Optional[str] = None):
        self.title = title
        super().__init__(self.name, contents, env_modifiers=self.env_modifiers)

    @property
    def env_modifiers(self):
        if self.title is not None:
            return f'{{{self.title}}}'

        return None