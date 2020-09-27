from typing import Optional, Union, TYPE_CHECKING, overload, Dict

if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay
    from pyexlatex.models.package import Package
    from pyexlatex.typing import PyexlatexItem

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
    _data_has_been_initialized = False

    def init_data(self):
        from pyexlatex.models.documentsetup import DocumentSetupData
        if not self._data_has_been_initialized:
            self._data_has_been_initialized = True
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

    @overload
    def _wrap_with(self, item: 'PyexlatexItem', begin_wrap: str, end_wrap: str,
                   format_contents: bool = True) -> str:
        ...
    @overload
    def _wrap_with(self, item: None, begin_wrap: str, end_wrap: str,
                   format_contents: bool = True) -> None:
        ...
    def _wrap_with(self, item, begin_wrap, end_wrap, format_contents=True):
        if format_contents:
            fmt = self._format_content
        else:
            fmt = lambda x: x

        if item is None:
            return None

        return f'{begin_wrap}{fmt(item)}{end_wrap}'

    @overload
    def _wrap_with_bracket(self, item: 'PyexlatexItem') -> str:
        ...
    @overload
    def _wrap_with_bracket(self, item: None) -> None:
        ...
    def _wrap_with_bracket(self, item):
        return self._wrap_with(item, '[', ']')

    @overload
    def _wrap_with_braces(self, item: 'PyexlatexItem') -> str:
        ...
    @overload
    def _wrap_with_braces(self, item: None) -> None:
        ...
    def _wrap_with_braces(self, item):
        return self._wrap_with(item, '{', '}')

    @staticmethod
    def _dict_to_options_str(d: Dict[str, 'PyexlatexItem']) -> str:
        return ','.join([f'{key}={value}' for key, value in d.items()])

    @staticmethod
    def _empty_str_if_none(item: Optional[str]) -> str:
        return item if item is not None else ''

    @staticmethod
    def _format_content(content):
        from pyexlatex.logic.format.contents import format_contents as fmt
        return fmt(content)

    @staticmethod
    def _get_list_copy_from_list_or_none(list_or_none: Optional[list]) -> list:
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
        from pyexlatex.models.environment import Environment
        self.env = Environment(name, modifiers=env_modifiers, overlay=overlay)
        self.contents = contents
        self.pre_env_contents = pre_env_contents
        self.post_env_contents = post_env_contents
        self.overlay = overlay
        super().__init__()

    def __repr__(self):
        return f'<Item(name={self.env.name}, contents={self.contents})>'

    def __str__(self):
        from pyexlatex.logic.builder import _build, build

        contents = deepcopy(self.contents)
        contents = build(contents)

        possible_items = [
            self.pre_env_contents,
            self.env.wrap(str(contents)),
            self.post_env_contents
        ]
        items = [item for item in possible_items if item]
        return _build(items)


class SimpleItem(ItemBase):
    equal_attrs = [
        'contents',
        'modifiers',
        'pre_modifiers',
        'overlay',
        'format_content',
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

    def __init__(self, name, overlay: Optional['Overlay'] = None, modifiers: Optional[str] = None):
        self.name = name
        self.overlay = overlay
        self.modifiers = modifiers
        super().__init__()

    def __repr__(self):
        return f'<{self.name.title()}>'

    def __str__(self):
        return no_options_no_contents_str(self.name, overlay=self.overlay, modifiers=self.modifiers)