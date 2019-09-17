from pyexlatex.models.control.documentclass.classtypes.documentclasstype import DocumentClassType

BUILTIN_CLASS_TYPE_NAMES = [
    'article',
    'report',
    'letter',
    'book',
    'proc',
    'slides',
    'beamer',
    'standalone',
]

BUILTIN_CLASS_TYPES = {style_str: DocumentClassType(style_str) for style_str in BUILTIN_CLASS_TYPE_NAMES}
