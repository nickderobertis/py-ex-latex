from pyexlatex.models.references.bibtex.style.builtin_styles import BUILTIN_STYLES
from pyexlatex.models.references.bibtex.style.custom import CUSTOM_STYLES
from pyexlatex.models.references.bibtex.style.style import Style

class StyleManager:

    def __init__(self):
        pass

    def get_style_by_name(self, name: str) -> Style:
        if self.is_builtin_style(name):
            return BUILTIN_STYLES[name]
        
        if self.is_custom_style(name):
            return CUSTOM_STYLES[name]

        raise NoSuchStyleException

    def is_custom_style(self, name: str) -> bool:
        return name in CUSTOM_STYLES

    def is_builtin_style(self, name: str) -> bool:
        return name in BUILTIN_STYLES


class NoSuchStyleException(Exception):
    pass
