from typing import List, Optional, Sequence
from pyexlatex.models.template import Template
from pyexlatex.models.title.title import Title
from pyexlatex.models.credits.author import Author
from pyexlatex.models.date import Date
from pyexlatex.models.section.abstract import Abstract
from pyexlatex.texgen import _maketitle_str
from pyexlatex.logic.format.and_join import join_with_commas_and_and
from pyexlatex.models.sizes.baselineskip import BaselineSkip
from pyexlatex.models.control.group import Group
from pyexlatex.models.control.setlength import SetLength
from pyexlatex.models.control.setcounter import SetCounter
from pyexlatex.models.format.text.bold import Bold
from pyexlatex.models.sizes.textsizes import TextSize
from pyexlatex.models.format.centering import Center
from pyexlatex.models.control.newpage import PageBreak
from pyexlatex.models.page.style import ThisPageStyle
from pyexlatex.models.format.vspace import VSpace
from pyexlatex.models.format.hspace import HSpace
from pyexlatex.models.format.breaks import LineBreak


class TitlePage(Template):

    def __init__(self, title: str = None, authors: List[str] = None, date: Optional[str] = None,
                 abstract: Optional[str] = None, separate_abstract_page: bool = False,
                 extra_lines: Optional[Sequence] = None, empty_page_style: bool = False):

        self.empty_page_style = empty_page_style
        self.title = title

        author: Optional[str]
        if authors is not None:
            author = join_with_commas_and_and(authors)
        else:
            author = None

        contents = [
            self._title_obj,
            Author(author, short_author=None) if author is not None else None,
            Date(date) if date is not None else Date(),
            _maketitle_str() if title is not None else None,
            ThisPageStyle('empty') if empty_page_style else None,
            Abstract(abstract) if abstract is not None and not separate_abstract_page else None,
        ]

        if extra_lines is not None and not separate_abstract_page:
            contents.extend(extra_lines)

        if separate_abstract_page and abstract:
            contents.append(
                CustomTitlePage(title, abstract, extra_lines=extra_lines, next_page_number=1)
            )

        self.contents = [content for content in contents if content is not None]

        super().__init__()

    @property
    def _title_obj(self) -> Optional[Title]:
        if self.title is None:
            return None

        title = self.title

        if self.empty_page_style:
            # Empty page style strips away bold title, bring it back manually
            title = Bold(title)

        return Title(title)


class CustomTitlePage(Template):
    r"""
    Title page which is not created using \maketitle, instead it is created manually and so may be included at
    any point in a document, and there may be multiple.
    """

    def __init__(self, title: Optional[str], abstract: Optional[str] = None, title_relative_size: int = 3,
                 gap_after_title_pt: int = 35, extra_lines: Optional[Sequence] = None,
                 next_page_number: Optional[int] = None):
        self.title = title
        self.abstract = abstract
        self.title_relative_size = title_relative_size
        self.gap_after_title = gap_after_title_pt
        self.extra_lines = extra_lines
        self.next_page_number = next_page_number

        self.contents = self._get_contents()
        super().__init__()

    def _get_contents(self):
        contents = [
            PageBreak(),
            ThisPageStyle('empty'),
            self._title_block,
            VSpace(self.gap_after_title, units='pt'),
        ]
        if self.abstract is not None:
            contents.extend(self._abstract_block)
        if self.extra_lines is not None:
            contents.extend(self._extra_lines_block)
        contents.append(PageBreak())
        if self.next_page_number is not None:
            contents.append(SetCounter('page', 1))
        return contents

    @property
    def _title_block(self) -> Group:
        main_contents = [
            SetLength(BaselineSkip(), '40pt'),
            TextSize(self.title_relative_size),
            Bold(self.title)
        ]
        return Group(Center(main_contents))

    @property
    def _abstract_block(self):
        if self.abstract is None:
            return None
        abstract_title = Center(Bold('Abstract'))
        return [
            abstract_title,
            VSpace(-10, 'pt'),
            HSpace(1.5, 'em'),
            self.abstract
        ]

    @property
    def _extra_lines_block(self):
        if self.extra_lines is None:
            return None
        contents = [VSpace(20, 'pt')]
        for line in self.extra_lines:
            contents.extend([
                line,
                LineBreak(),
            ])
        return contents






