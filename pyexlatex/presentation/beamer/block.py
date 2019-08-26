from typing import Optional
from pyexlatex.models.section.base import TextAreaBase
from pyexlatex.presentation.beamer.theme.setcolor import SetBeamerColor


class BlockBase(TextAreaBase):
    name = '<invalid, use a subclass, not BlockBase>'

    def __init__(self, content, title: Optional[str] = None, text_color: Optional[str] = None,
                 header_color: Optional[str] = None, **kwargs):
        self.content = content
        self.title = title
        title_str = title if title is not None else ''
        title_modifier_str = f'{{{title_str}}}'

        pre_env_contents = None
        post_env_contents = None
        if text_color is not None or header_color is not None:
            from pyexlatex.logic.builder import _build
            color_options = []
            if text_color is not None:
                color_options.append(f'fg={text_color}')
            if header_color is not None:
                color_options.append(f'bg={header_color}')
            set_color = SetBeamerColor('block title', color_options)
            pre_env_contents = _build([
                '{',
                set_color
            ])
            post_env_contents = '}'


        super().__init__(self.name, self.content, env_modifiers=title_modifier_str,
                         pre_env_contents=pre_env_contents,
                         post_env_contents=post_env_contents, **kwargs)


class Block(BlockBase):
    """
    Block with an optional header
    """
    name = 'block'


class AlertBlock(BlockBase):
    """
    Block with an optional header which is red
    """
    name = 'alertblock'


class ExamplesBlock(BlockBase):
    """
    Block which always has the header title "Examples"
    """
    name = 'examples'

    def __init__(self, content):
        super().__init__(content, None)  # examples does not support a title
