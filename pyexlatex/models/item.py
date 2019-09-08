from typing import Optional, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay import Overlay
    from pyexlatex.models.package import Package
from copy import deepcopy
from mixins.attrequals import EqOnAttrsMixin, EqHashMixin
from pyexlatex.models.mixins import StringAdditionMixin, IsSpecificClassMixin
from pyexlatex.texgen import (
    _basic_item_str,
    _multi_option_item_str,
    _no_braces_item_str,
    item_equals_str,
    no_options_no_contents_str
)



class IsLatexItemMixin:
    is_LatexItem = True


class DataItem:
    def init_data(self):
        from pyexlatex.models.documentsetup import DocumentSetupData
        if not hasattr(self, 'data'):
            self.data = DocumentSetupData()

    def add_package(self, package: Union[str, 'Package']):
        self.init_data()
        self.data.packages.append(package)


class ItemBase(DataItem, IsSpecificClassMixin, IsLatexItemMixin, StringAdditionMixin, EqHashMixin, EqOnAttrsMixin):
    """
    Base class for all latex generating classes
    
    Note: Does not pass any args to super call, so do not put another class below this one expecting args to
    be passed
    """
    

    def __init__(self, *args, **kwargs):
        self.init_data()
        super().__init__()

    def _wrap_with(self, item: Optional[str], begin_wrap: str, end_wrap: str,
                   format_contents: bool = True) -> Optional[str]:
        if format_contents:
            fmt = self._format_content
        else:
            fmt = lambda x: x

        if item is None:
            return None

        return f'{begin_wrap}{fmt(item)}{end_wrap}'

    def _wrap_with_bracket(self, item: Optional[str]) -> Optional[str]:
        return self._wrap_with(item, '[', ']')

    def _wrap_with_braces(self, item: Optional[str]) -> Optional[str]:
        return self._wrap_with(item, '{', '}')

    @staticmethod
    def _empty_str_if_none(item: Optional[str]) -> str:
        return item if item is not None else ''

    @staticmethod
    def _format_content(content):
        from pyexlatex.logic.format.contents import format_contents as fmt
        return fmt(content)

    @staticmethod
    def _get_list_copy_from_list_or_none(list_or_none: Optional[list]):
        if list_or_none is None:
            return []
        return deepcopy(list_or_none)




class Item(ItemBase):
    equal_attrs = [
        'contents',
        'pre_env_contents',
        'post_env_contents',
        'data',
        'env'
    ]

    def __init__(self, name, contents, pre_env_contents=None, post_env_contents=None, env_modifiers=None,
                 overlay: Optional['Overlay'] = None):
        from pyexlatex.models import Environment
        self.env = Environment(name, modifiers=env_modifiers, overlay=overlay)
        self.contents = contents
        self.pre_env_contents = pre_env_contents
        self.post_env_contents = post_env_contents
        self.overlay = overlay
        super().__init__()

    def __repr__(self):
        return f'<Item(name={self.env.name}, contents={self.contents})>'

    def __str__(self):
        from pyexlatex.logic.builder import _build
        possible_items = [
            self.pre_env_contents,
            self.env.wrap(str(self.contents)),
            self.post_env_contents
        ]
        items = [item for item in possible_items if item]
        return _build(items)


class SimpleItem(ItemBase):
    equal_attrs = [
        'contents',
        'pre_env_contents',
        'post_env_contents',
        'data'
    ]

    def __init__(self, name, contents, modifiers: Optional[str] = None, pre_modifiers: Optional[str] = None,
                 overlay: Optional['Overlay'] = None, format_content: bool = True):
        self.name = name
        self.contents = contents
        self.modifiers = modifiers
        self.pre_modifiers = pre_modifiers
        self.overlay = overlay
        self.format_content = format_content
        super().__init__()

    def __repr__(self):
        return f'<{self.name.title()}({self.contents})>'

    def __str__(self):
        return _basic_item_str(
            self.name,
            self.contents,
            self.modifiers,
            self.pre_modifiers,
            overlay=self.overlay,
            format_content=self.format_content
        )


class MultiOptionSimpleItem(ItemBase):

    def __init__(self, name, *options, overlay: Optional['Overlay'] = None):
        self.name = name
        self.options = options
        self.overlay = overlay
        super().__init__()

    def __repr__(self):
        return f'<{self.name.title()}({self.options})>'

    def __str__(self):
        return _multi_option_item_str(self.name, *self.options, overlay=self.overlay)


class NoBracesItem(ItemBase):

    def __init__(self, name, contents, overlay: Optional['Overlay'] = None):
        self.name = name
        self.contents = contents
        self.overlay = overlay
        super().__init__()

    def __repr__(self):
        return f'<{self.name.title()}({self.contents})>'

    def __str__(self):
        return _no_braces_item_str(self.name, self.contents, overlay=self.overlay)


class EqualsItem(ItemBase):

    def __init__(self, name, contents):
        self.name = name
        self.contents = contents
        super().__init__()

    def __repr__(self):
        return f'<{self.name.title()}({self.contents})>'

    def __str__(self):
        return item_equals_str(self.name, self.contents)


class NoOptionsNoContentsItem(ItemBase):

    def __init__(self, name, overlay: Optional['Overlay'] = None):
        self.name = name
        self.overlay = overlay
        super().__init__()

    def __repr__(self):
        return f'<{self.name.title()}>'

    def __str__(self):
        return no_options_no_contents_str(self.name, overlay=self.overlay)