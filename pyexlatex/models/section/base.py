from typing import Optional, Type, TYPE_CHECKING, cast

from pyexlatex.typing import PyexlatexItems, PyexlatexItem

if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay

from pyexlatex.models.environment import Environment
from pyexlatex.models.item import Item
from mixins.repr import ReprMixin
from pyexlatex.logic.format.contents import format_contents as fmt
from pyexlatex.logic.builder import _build
from pyexlatex.models.documentitem import DocumentItem
from pyexlatex.models.label import Label
from pyexlatex.models.containeritem import ContainerItem


class TextAreaMixin(ContainerItem):
    """
    Mixin for extracting data from content then formatting it, regardless of the data type passed
    """
    name = 'textarea'
    next_level_down_class: Optional[Type['TextAreaBase']] = None  # once subclassed, will be overridden with the next level down text area class

    def __init__(self, name, contents, label: Optional[str] = None, **kwargs):
        self.add_data_from_content(contents)
        contents = self.format_contents(contents)
        if label is not None:
            label = Label(label)
            if not isinstance(contents, (list, tuple)):
                contents = [contents]
            contents = contents + [label]
        self.contents = contents
        super().__init__(name, contents, **kwargs)

    def format_contents(self, contents):
        if isinstance(contents, (list, tuple)):
            return [self.format_contents(c) for c in contents]
        elif isinstance(contents, dict):
            if self.next_level_down_class is None:
                raise ValueError(f'cannot parse dict as have no next_level_down_class in {self.__class__.name}')
            subcontents = []
            for title, content in contents.items():
                subcontents.append(
                    self.next_level_down_class(content, title=title)
                )
            return subcontents
        else:
            # Not an iterable
            return self._format_content(contents)

    def format_contents_and_build(self, contents: PyexlatexItems):
        contents = self.format_contents(contents)
        return self._build(contents)

    def _build(self, contents: PyexlatexItems) -> PyexlatexItem:
        if isinstance(contents, (list, tuple)):
            contents = [self._build(c) for c in contents]
            return _build(contents)
        contents = cast(PyexlatexItem, contents)
        return contents

    def _format_content(self, content):
        if isinstance(content, str):
            return fmt(content)
        else:
            # Class is responsible for formatting. This may be a latex class or some
            # other harmless conversion such as int. It may also be an issue if the __str__
            # method of the class is not valid latex
            return content


class EnvironmentTextArea(TextAreaMixin, Environment):

    def __init__(self, name, modifiers: Optional[str] = None, overlay: Optional['Overlay'] = None):
        Environment.__init__(self, name, modifiers=modifiers, overlay=overlay)

    def wrap(self, other):
        self.add_data_from_content(other)
        contents = self.format_contents_and_build(other)

        return super().wrap(contents)


class TextAreaBase(TextAreaMixin, Item, ReprMixin):
    repr_cols = ['title', 'contents']


class SectionBase(TextAreaBase):
    name = 'section'
    repr_cols = ['title', 'short_title', 'contents']

    def __init__(self, contents, title: str, short_title: Optional[str] = None, **kwargs):
        self.title = title
        self.short_title = short_title
        super().__init__(self.name, contents, env_modifiers=self.env_modifiers, **kwargs)

    @property
    def env_modifiers(self):
        modifier_str = ''
        if self.short_title is not None:
            modifier_str += f'[{fmt(self.short_title)}]'

        modifier_str += f'{{{fmt(self.title)}}}'

        return modifier_str


class ParagraphBase(TextAreaBase):
    name = 'paragraph'
    repr_cols = ['title', 'contents']

    def __init__(self, contents, title: Optional[str] = None, **kwargs):
        self.title = title
        super().__init__(self.name, contents, env_modifiers=self.env_modifiers, **kwargs)

    @property
    def env_modifiers(self):
        if self.title is not None:
            return f'{{{self.title}}}'

        return None