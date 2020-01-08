from typing import Dict, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay


def _include_graphics_str(filepath, width=r'\linewidth'):
    return rf'\includegraphics[width={width}]{{{filepath}}}'


def _bracket_modifier_str(modifiers: Optional[str] = None) -> str:
    if modifiers is None:
        return ''

    return f'[{modifiers}]'

def no_options_no_contents_str(item_name: str, overlay: Optional['Overlay'] = None,
                               modifiers: Optional[str] = None) -> str:
    overlay_str = str(overlay) if overlay is not None else ""
    modifiers = modifiers if modifiers is not None else ""
    return rf'\{item_name}{overlay_str}{modifiers}'


def _no_braces_item_str(item_name, contents, overlay: Optional['Overlay'] = None) -> str:
    from pyexlatex.logic.format.contents import format_contents
    overlay_str = str(overlay) if overlay is not None else ""
    return rf'\{item_name}{overlay_str} {format_contents(contents)}'


def _basic_item_str(item_name, contents, modifiers: Optional[str] = None, pre_modifiers: Optional[str] = None,
                    overlay: Optional['Overlay'] = None, format_content: bool = True):
    from pyexlatex.logic.format.contents import format_contents
    pre_modifiers = pre_modifiers if pre_modifiers is not None else ""
    modifiers = modifiers if modifiers is not None else ""
    overlay_str = str(overlay) if overlay is not None else ""

    if format_content:
        contents = format_contents(contents)

    return rf'\{item_name}{overlay_str}{pre_modifiers}{{{contents}}}{modifiers}'


def _multi_option_item_str(item_name, *options, overlay: Optional['Overlay'] = None):
    from pyexlatex.logic.format.contents import format_contents
    overlay_str = str(overlay) if overlay is not None else ""
    options_str = ''.join([f'{{{format_contents(str(option))}}}' for option in options])
    return rf'\{item_name}{overlay_str}{options_str}'


def item_equals_str(item_name, contents):
    return rf'\{item_name}={contents}'


def _cmidrule_str(align, col_str):
    return _multi_option_item_str(rf'cmidrule({align})', col_str)

def _centering_str():
    return r'\centering'

def _toprule_str():
    return r'\toprule'

def _midrule_str():
    return r'\midrule'

def _bottomrule_str():
    return r'\bottomrule'

def _maketitle_str():
    return r'\maketitle'

def _todays_date_str():
    return r'\today'


def _usepackage_str(str_, modifier_str=None):
    if modifier_str:
        full_modifier_str = f'[{modifier_str}]'
    else:
        full_modifier_str = ''
    return rf'\usepackage{full_modifier_str}{{{str_}}}'


def bibtex_str(item_type: str, item_accessor: str, fields: Dict[str, str]) -> str:
    from pyexlatex.logic.builder import _build
    begin_str = f'@{item_type}{{{item_accessor},'
    field_strs = ['    ' + _bibtex_field_str(key, value) for key, value in fields.items()]
    end_str = '}'
    full_str = _build([
        begin_str,
        *field_strs,
        end_str
    ])

    return full_str


def _bibtex_field_str(key: str, value: str) -> str:
    from pyexlatex.logic.format.contents import format_contents
    return f'{key} = {{{format_contents(value)}}},'
