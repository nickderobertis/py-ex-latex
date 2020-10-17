"""
Create LaTeX documents using only Python. Rather than building a direct Python API to LaTeX, this package
has its own, simpler API to creating documents. It is focused on creating professional-looking documents
with little styling effort. It currently supports documents, presentations, graphics, letters, and resumes.
"""
from pyexlatex.models.document import Document
from pyexlatex.models.standalone import Standalone
from pyexlatex.letter.letterdocument import LetterDocument
from pyexlatex.models.equation import Equation
from pyexlatex.models.section.paragraphs import Paragraph, SubParagraph
from pyexlatex.models.section.sections import Section, SubSection, SubSubSection
from pyexlatex.models.section.appendix import Appendix
from pyexlatex.models.lists.unordered import UnorderedList
from pyexlatex.models.lists.ordered import OrderedList
from pyexlatex.models.format.raw import Raw
from pyexlatex.models.format.text.text import Text
from pyexlatex.models.ref import Ref, NameRef
from pyexlatex.models.footnote import Footnote
from pyexlatex.models.references.bibtex.article import BibTexArticle
from pyexlatex.models.references.bibtex.misc import BibTexMisc
from pyexlatex.models.references.bibtex.manual import BibTexManual
from pyexlatex.models.references.bibliography import Bibliography
from pyexlatex.models.references.citations import Cite, CiteP, CiteT
from pyexlatex.models.format.text.color.main import TextColor
from pyexlatex.models.format.text.monospace import Monospace
from pyexlatex.models.format.text.underline import Underline
from pyexlatex.models.format.text.bold import Bold
from pyexlatex.models.format.text.italics import Italics
from pyexlatex.models.format.text.smallcaps import SmallCaps
from pyexlatex.models.format.code.python import Python
from pyexlatex.figure.models.graphic import Graphic
from pyexlatex.figure.models.inlinegraphic import InlineGraphic
from pyexlatex.models.format.fills import VFill, HFill
from pyexlatex.models.hyperlinks import Hyperlink
from pyexlatex.models.package import Package
from pyexlatex.models.page.header import Header
from pyexlatex.models.page.footer import LeftFooter, RightFooter, CenterFooter, FooterLine
from pyexlatex.models.page.number import ThisPageNumber
from pyexlatex.models.format.vspace import VSpace
from pyexlatex.models.format.hspace import HSpace
from pyexlatex.models.format.paragraphindent import ParagraphIndent
from pyexlatex.models.format.hline import HLine
from pyexlatex.models.format.text.color.deftypes.rgb import RGB
from pyexlatex.models.format.text.color.deftypes.hex import Hex
from pyexlatex.models.template import Template
from pyexlatex.models.environmenttemplate import EnvironmentTemplate
from pyexlatex.models.format.breaks import OutputLineBreak
from pyexlatex.models.latex import LaTeX
from pyexlatex.models.format.nopagebreak import NoPageBreak
from pyexlatex.models.format.nolinebreak import NoLineBreak
from pyexlatex.models.format.paragraph.justifying import Justifying
from pyexlatex.models.format.centering import Center
from pyexlatex.models.format.captionsetup import CaptionSetup
from pyexlatex.models.control.newpage import PageBreak
from pyexlatex.models.control.group import Group
from pyexlatex.models.sizes.textsizes import TextSize
from pyexlatex.models.toc import TableOfContents
from pyexlatex.models.jinja import JinjaEnvironment, JinjaTemplate
from pyexlatex.models.model import Model

from pyexlatex.table.models.panels import Panel
from pyexlatex.table.models.data.table import DataTable
from pyexlatex.table.models.labels.table import LabelCollection, LabelTable
from pyexlatex.table.models.labels.label import Label
from pyexlatex.table.models.table.table import Table
from pyexlatex.table.models.texgen.items import Tabular
from pyexlatex.table.models.data.valuestable import ValuesTable
from pyexlatex.table.models.texgen.alignment import ColumnAlignment, ColumnsAlignment
from pyexlatex.table.models.texgen.lines import TopRule, MidRule, BottomRule, TableLineSegment
from pyexlatex.table.models.labels.multicolumnlabel import MultiColumnLabel
from pyexlatex.models.format.breaks import TableLineBreak
from pyexlatex.table.models.texgen.tabularstar import TabularStar

from pyexlatex.figure.models.figure import Figure
from pyexlatex.figure.models.subfigure import Subfigure

from pyexlatex.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.presentation.beamer.overlay.range import Range
from pyexlatex.presentation.beamer.overlay.next import NextWithIncrement, NextWithoutIncrement
from pyexlatex.presentation.beamer.overlay.until_end import UntilEnd
from pyexlatex.presentation.beamer.frame.frame import Frame
from pyexlatex.presentation.beamer.block import Block, AlertBlock, ExamplesBlock
from pyexlatex.presentation.presentation import Presentation
from pyexlatex.presentation.beamer.templates.frames.grid import GridFrame
from pyexlatex.presentation.beamer.templates.lists.dim_reveal_items import DimAndRevealListItems, DimAndRevealListItem
from pyexlatex.presentation.beamer.templates.frames.two_col import (
    TwoColumnGraphicDimRevealFrame,
    TwoColumnGraphicFrame,
    BasicTwoColumnGraphicFrame,
    BasicTwoColumnFrame,
    TwoColumnFrame
)
from pyexlatex.presentation.beamer.templates.frames.dim_reveal import DimRevealListFrame
from pyexlatex.presentation.beamer.templates.frames.graphic import (
    GraphicFrame,
    MultiGraphicFrame,
)
from pyexlatex.logic.format.sizing import adjust_to_full_size_and_center
from pyexlatex.presentation.beamer.templates.presentationappendix import PresentationAppendix

from pyexlatex.layouts.grid import CellLayout, GridLayout
from pyexlatex.layouts.multicol import MultiCol
from pyexlatex.layouts.spaced import VerticallySpaced, HorizontallySpaced
from pyexlatex.models.format.paragraph.multicol import MultiColumn

