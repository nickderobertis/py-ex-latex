from typing import Optional
from dero.latex.models.section.base import TextAreaMixin
from dero.latex.models.item import SimpleItem


# TODO: update all of this after getting a better understanding of how boxes work and the syntax.
# TODO: see: https://en.wikibooks.org/wiki/LaTeX/Boxes
class BoxBase(TextAreaMixin, SimpleItem):
    name = '<unimplemented, do not use BoxBase directly, use a subclass>'

    def __init__(self, contents, size_str: Optional[str]):
        super().__init__(self.name, contents, pre_modifiers=size_str, format_content=False)
