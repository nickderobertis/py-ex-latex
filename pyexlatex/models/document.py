from typing import List, Optional, Dict, Union, Sequence, Callable
from copy import deepcopy

from pyexlatex.models.environment import Environment
from pyexlatex.models.item import Item, ItemBase
from pyexlatex.models.control.documentclass.documentclass import DocumentClass
from pyexlatex.models.package import Package
from pyexlatex.models.page.style import PageStyle
from pyexlatex.models.landscape import Landscape
from pyexlatex.logic.pdf.main import document_to_pdf_and_move, latex_str_to_pdf_obj_with_sources
from pyexlatex.texgen.replacements.filename import latex_filename_replacements
from pyexlatex.logic.extract.docitems import extract_document_items_from_ambiguous_collection
from pyexlatex.models.page.number import right_aligned_page_numbers
from pyexlatex.models.page.header import remove_header
from pyexlatex.models.page.footer import CenterFooter
from pyexlatex.models.format.sectionnum import SectionNumberingFormatter
from pyexlatex.typing import AnyItem, ItemOrListOfItems, ItemAndPreEnvContents
from pyexlatex.models.commands.endfloat import DeclareDelayedFloatFlavor
from pyexlatex.models.format.text.linespacing import LineSpacing
from pyexlatex.models.commands.floatrow import DeclareFloatFont, FloatSetup
from pyexlatex.models.containeritem import ContainerItem
from pyexlatex.models.page.header import Header
from pyexlatex.models.control.setcounter import SetCounter


class DocumentEnvironment(Environment):
    name = 'document'

    def __init__(self):
        super().__init__(name=self.name)


class DocumentBase(ContainerItem, Item):
    name = '<invalid, do not use DocumentBase directly>'
    document_class_obj = None

    def __init__(self, content: ItemOrListOfItems, packages: List[Package]=None,
                 pre_env_contents: Optional[ItemOrListOfItems] = None, data_cleanup_func: Optional[Callable] = None):
        """

        :param content:
        :param packages:
        :param pre_env_contents:
        :param data_cleanup_func: should accept DocumentSetupData and modify it in place. This is called just before
            using the data.
        """
        from pyexlatex.logic.builder import build, _build
        self.add_data_from_content(content)
        self.add_data_from_content(self.document_class_obj)

        if packages is not None:
            self.data.packages.extend(packages)

        self.has_references = False
        if self.data.references:
            self.has_references = True

        if isinstance(content, (ItemBase, str)):
            content = [content]

        if pre_env_contents is None:
            pre_env_contents = []

        if data_cleanup_func:
            data_cleanup_func(self.data)

        possible_pre_env_contents = [
            self.document_class_obj,
            *self.data.begin_document_items,
            *[str(package) for package in self.data.packages],
            *pre_env_contents
        ]

        self.pre_env_contents = _build([item for item in possible_pre_env_contents if item is not None])

        content.extend(self.data.end_document_items)

        self.contents = content


        content = deepcopy(content)  # don't overwrite original objects
        # combine content into a single str
        content = build(content)

        super().__init__(self.name, content, pre_env_contents=self.pre_env_contents)

    def _repr_pdf_(self):
        tex = str(self)

        return latex_str_to_pdf_obj_with_sources(
            tex,
            image_paths=self.data.filepaths,
            image_binaries=self.data.binaries,
            run_bibtex=self.has_references
        ).readb()

    def to_pdf(self, outfolder, outname='document',
               move_folder_name='Tables', as_document=True,
               date_time_move: bool = False):
        tex = str(self)

        outname = latex_filename_replacements(outname)

        document_to_pdf_and_move(
            tex,
            outfolder=outfolder,
            outname=outname,
            image_paths=self.data.filepaths,
            move_folder_name=move_folder_name,
            as_document=as_document,
            image_binaries=self.data.binaries,
            run_bibtex=self.has_references,
            date_time_move=date_time_move
        )

    @classmethod
    def from_ambiguous_collection(cls, collection, **document_kwargs):
        content = extract_document_items_from_ambiguous_collection(collection)

        return cls(content, **document_kwargs)


class Document(DocumentBase):
    """
    Main class used for creating latex documents, use for all except presentations.
    """
    name = 'document'

    def __init__(self, content: ItemOrListOfItems, packages: List[Package]=None, landscape=False,
                 title: str=None, authors: Optional[Union[List[str], str]] = None, date: str=None, abstract: str=None,
                 skip_title_page: bool=False,
                 page_modifier_str: Optional[str]='margin=0.8in, bottom=1.2in', page_header: bool=False,
                 page_numbers: bool=True, appendix_modifier_str: Optional[str] = 'page',
                 section_numbering_styles: Optional[Dict[str, str]] = None, floats_at_end: bool = False,
                 floats_at_end_options: str = 'nolists',
                 document_type: str = 'article', font_size: Optional[float] = None,
                 num_columns: Optional[int] = None, line_spacing: Optional[float] = None,
                 tables_relative_font_size: int = 0, figures_relative_font_size: int = 0,
                 page_style: str = 'fancy', custom_headers: Optional[Sequence[Header]] = None,
                 remove_section_numbering: bool = False, separate_abstract_page: bool = False,
                 extra_title_page_lines: Optional[Sequence] = None, empty_title_page_style: bool = False):
        from pyexlatex.models.title.page import TitlePage

        all_packages = self.construct_packages(
            packages=packages,
            page_modifier_str=page_modifier_str,
            appendix_modifier_str=appendix_modifier_str,
            floats_at_end=floats_at_end,
            floats_at_end_options=floats_at_end_options,
            line_spacing=line_spacing,
            tables_relative_font_size=tables_relative_font_size,
            figures_relative_font_size=figures_relative_font_size
        )

        if section_numbering_styles is None:
            section_numbering_styles = {}

        section_num_styles = SectionNumberingFormatter.list_from_string_format_dict(section_numbering_styles)

        if isinstance(content, (Item, str)):
            content = [content]
        if authors is None:
            authors = []
        if custom_headers is None:
            custom_headers = []
        if isinstance(authors, (Item, str)):
            authors = [authors]

        self.document_class_obj = DocumentClass(
            document_type=document_type,
            font_size=font_size,
            num_columns=num_columns
        )

        possible_extra_pre_env_contents = [
            *section_num_styles,
            SetCounter('secnumdepth', 0) if remove_section_numbering else None,
            PageStyle(page_style),

            # header is there by default. add remove header lines if page_header=False
            remove_header if not page_header and not custom_headers else None,
            *custom_headers,

            # add right page numbers. if not, use blank center footer to clear default page numbers in center footer
            right_aligned_page_numbers if page_numbers else CenterFooter('')
        ]

        pre_env_contents = [item for item in possible_extra_pre_env_contents if item is not None]

        if not skip_title_page and _should_create_title_page(title=title, authors=authors, date=date, abstract=abstract):
            title_page = TitlePage(
                title=title,
                authors=authors,
                date=date,
                abstract=abstract,
                separate_abstract_page=separate_abstract_page,
                extra_lines=extra_title_page_lines,
                empty_page_style=empty_title_page_style
            )
            content.insert(0, title_page)
            self.has_title_page = True
        else:
            self.has_title_page = False

        if landscape:
            content = Landscape().wrap(content)

        super().__init__(content, packages=all_packages, pre_env_contents=pre_env_contents)

    def __repr__(self):
        return f'<Document>'

    def construct_packages(self, packages: List[Package]=None,
                           page_modifier_str: Optional[str]='margin=0.8in, bottom=1.2in',
                           appendix_modifier_str: Optional[str] = 'page',
                           floats_at_end: bool = False, floats_at_end_options: str = 'nolists',
                           line_spacing: Optional[float] = None,
                           tables_relative_font_size: int = 0, figures_relative_font_size: int = 0) -> List[Package]:
        from pyexlatex.texgen.packages.default import default_packages

        if packages is None:
            packages = default_packages.copy()

        if page_modifier_str is not None:
            # Set margins, body size, etc. with geometry package
            packages.append(Package('geometry', modifier_str=page_modifier_str))

        if tables_relative_font_size or figures_relative_font_size:
            packages.append(Package('floatrow'))
            if tables_relative_font_size:
                declared_font = DeclareFloatFont(tables_relative_font_size)
                float_setup_str = f'font={declared_font.size_def.name},capposition=top'
                packages.extend([
                    declared_font,
                    FloatSetup('table', float_setup_str),
                    # FloatSetup('ltable', float_setup_str)
                ])
            if figures_relative_font_size:
                declared_font = DeclareFloatFont(figures_relative_font_size)
                float_setup_str = f'font={declared_font.size_def.name},capposition=top'
                packages.extend([
                    declared_font,
                    FloatSetup('figure', float_setup_str),
                    # FloatSetup('lfigure', float_setup_str)
                ])

        if floats_at_end:
            packages.extend([
                Package('endfloat', modifier_str=floats_at_end_options if floats_at_end_options else None),
                DeclareDelayedFloatFlavor('ltable', 'table'),  # treat custom environment ltable (landscape table) as table
                DeclareDelayedFloatFlavor('lfigure', 'figure') # treat custom environment lfigure (landscape figure) as figure
            ])

        if line_spacing:
            packages.extend([
                Package('setspace'),
                LineSpacing(line_spacing)
            ])

        packages.append(Package('appendix', modifier_str=appendix_modifier_str))

        return packages


def _should_create_title_page(title: str = None, authors: Optional[List[str]] = None, date: str = None,
                              abstract: str = None):
    return any([
        title is not None,
        authors is not None and authors != [],
        date is not None,
        abstract is not None
    ])

def _content_items_and_collected_pre_env_contents():
    raise NotImplementedError('see TODO in _standardize_content_item_for_inclusion_in_document')

def _standardize_content_item_for_inclusion_in_document(item: AnyItem) -> ItemAndPreEnvContents:

    # No extra processing needed if not Document
    if not isinstance(item, Document):
        return item, None

    # TODO: restructure to remove title pages
    # TODO: restructure to extract content from Document

    return item, item.pre_env_contents

