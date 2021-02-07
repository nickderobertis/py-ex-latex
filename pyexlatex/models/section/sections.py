from pyexlatex.models.section.base import SectionBase
from pyexlatex.models.section.paragraphs import Paragraph


class SubSubSection(SectionBase):
    """
    A part of a subsection, the fourth largest section type.
    """
    name = 'subsubsection'
    next_level_down_class = Paragraph


class SubSection(SectionBase):
    """
    A part of a section, the third largest section type.
    """
    name = 'subsection'
    next_level_down_class = SubSubSection


class Section(SectionBase):
    """
    A section of the document, the second largest section type.
    """
    name = 'section'
    next_level_down_class = SubSection


class Chapter(SectionBase):
    """
    A chapter of the document, the largest section type

    Note: Not supported in all document types. 'report' is one
    type which can support it
    """
    name = 'chapter'
    next_level_down_class = Section
