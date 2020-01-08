from pyexlatex.models.section.base import ParagraphBase


class SubParagraph(ParagraphBase):
    """
    Part of a paragraph, the smallest section block.
    """
    name = 'subparagraph'


class Paragraph(ParagraphBase):
    """
    A paragraph, the second smallest section block.
    """
    name = 'paragraph'
    next_level_down_class = SubParagraph


