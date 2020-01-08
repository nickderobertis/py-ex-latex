from pyexlatex.models.item import NoOptionsNoContentsItem
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.models.format.breaks import LineBreak


class NoIndent(TextAreaMixin, NoOptionsNoContentsItem):
    """
    Do not have an indent for the current paragraph
    """
    name = 'noindent'

    def __init__(self, contents, **kwargs):
        TextAreaMixin.__init__(self, self.name, contents)
        NoOptionsNoContentsItem.__init__(self, self.name, **kwargs)
        if not isinstance(self.contents, (list, tuple)):
            self.contents = [self.contents]

    def __str__(self):
        from pyexlatex.logic.builder import _build
        from pyexlatex.texgen import no_options_no_contents_str
        if isinstance(self.contents, str):
            return self.contents
        # Ending line break is necessary to end paragraph, so that next item doesn't have no indent
        return no_options_no_contents_str(self.name, overlay=self.overlay) + _build(self.contents + [LineBreak()])
