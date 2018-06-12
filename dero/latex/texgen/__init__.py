def _begin_str(str_):
    return rf'\begin{{{str_}}}'


def _end_str(str_):
    return fr'\end{{{str_}}}'


def _include_graphics_str(filepath, width=r'\linewidth'):
    return rf'\includegraphics[width={width}]{{{filepath}}}'

def _basic_item_str(item_name, contents):
    return rf'\{item_name}{{{general_latex_replacements(contents)}}}'

def _multi_option_item_str(item_name, *options):
    options_str = ''.join([f'{{{general_latex_replacements(str(option))}}}' for option in options])
    return rf'\{item_name}{options_str}'

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


def _usepackage_str(str_, modifier_str=None):
    if modifier_str:
        full_modifier_str = f'[{modifier_str}]'
    else:
        full_modifier_str = ''
    return rf'\usepackage{full_modifier_str}{{{str_}}}'


def general_latex_replacements(string):
    return string.replace('&','\&').replace('%','\%').replace('_','\_')