from pyexlatex.models.references.bibtex.style.style import Style

BUILTIN_STYLE_NAMES = [
    'abbrv',
    'acm',
    'alpha',
    'apalike',
    'ieeetr',
    'plain',
    'siam',
    'unsrt',
]

BUILTIN_STYLES = {style_str: Style(style_str) for style_str in BUILTIN_STYLE_NAMES}