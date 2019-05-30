from typing import Dict


def _begin_str(str_):
    return rf'\begin{{{str_}}}'


def _end_str(str_):
    return fr'\end{{{str_}}}'


def _include_graphics_str(filepath, width=r'\linewidth'):
    return rf'\includegraphics[width={width}]{{{filepath}}}'


def no_options_no_contents_str(item_name: str) -> str:
    return rf'\{item_name}'


def _no_braces_item_str(item_name, contents) -> str:
    from dero.latex.logic.format.contents import format_contents
    return rf'\{item_name} {format_contents(contents)}'


def _basic_item_str(item_name, contents):
    from dero.latex.logic.format.contents import format_contents
    return rf'\{item_name}{{{format_contents(contents)}}}'

def _multi_option_item_str(item_name, *options):
    from dero.latex.logic.format.contents import format_contents
    options_str = ''.join([f'{{{format_contents(str(option))}}}' for option in options])
    return rf'\{item_name}{options_str}'


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

def _document_class_str():
    return r'\documentclass{article}'

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
    from dero.latex.logic.builder import _build
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
    from dero.latex.logic.format.contents import format_contents
    return f'{key} = {{{format_contents(value)}}},'
