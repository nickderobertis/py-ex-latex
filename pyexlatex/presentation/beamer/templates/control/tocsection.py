from pyexlatex.models.template import Template
from pyexlatex.presentation import Frame
from pyexlatex.presentation.beamer.control.atbeginsection import AtBeginSection
from pyexlatex.presentation.beamer.toc import TableOfContents


class TableOfContentsAtBeginSection(Template):

    def __init__(self):
        toc = TableOfContents()
        frame = Frame([toc], title='Table of Contents')
        at_begin = AtBeginSection(frame)
        self.contents = at_begin
        super().__init__()
