def _begin_str(str_):
    return rf'\begin{{{str_}}}'


def _end_str(str_):
    return fr'\end{{{str_}}}'


def _include_graphics_str(filepath, width=r'\linewidth'):
    return rf'\includegraphics[width={width}]{{{filepath}}}'

def _basic_item_str(item_name, contents):
    return rf'\{item_name}{{{contents}}}'

def _centering_str():
    return r'\centering'

def _document_class_str():
    return r'\documentclass{article}'