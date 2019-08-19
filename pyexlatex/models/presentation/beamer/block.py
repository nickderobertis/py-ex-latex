from typing import Optional
from pyexlatex.models.section.base import TextAreaBase


class BlockBase(TextAreaBase):
    name = '<invalid, use a subclass, not BlockBase>'

    def __init__(self, content, title: Optional[str] = None):
        self.content = content
        self.title = title
        title_str = title if title is not None else ''
        title_modifier_str = f'{{{title_str}}}'
        super().__init__(self.name, self.content, env_modifiers=title_modifier_str)


class Block(BlockBase):
    name = 'block'


class AlertBlock(BlockBase):
    name = 'alertblock'


class ExamplesBlock(BlockBase):
    name = 'examples'

    def __init__(self, content):
        super().__init__(content, None)  # examples does not support a title
