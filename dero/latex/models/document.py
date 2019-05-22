from typing import List, Optional, Dict, Sequence

from dero.latex.models.environment import Environment
from dero.latex.models import Item
from dero.latex.models.documentitem import DocumentItem
from dero.latex.texgen import _document_class_str
from dero.latex.models.package import Package
from dero.latex.texgen.packages import default_packages
from dero.latex.models.page.style import PageStyle
from dero.latex.models.landscape import Landscape
from dero.latex.logic.pdf.main import document_to_pdf_and_move, latex_str_to_pdf_obj_with_sources
from dero.latex.texgen.replacements.filename import latex_filename_replacements
from dero.latex.logic.extract.docitems import extract_document_items_from_ambiguous_collection
from dero.latex.models.page.number import right_aligned_page_numbers
from dero.latex.models.page.header import remove_header
from dero.latex.models.page.footer import CenterFooter
from dero.latex.models.format.sectionnum import SectionNumberingFormatter
from dero.latex.typing import AnyItem, ListOfItems, ItemOrListOfItems, StrListOrNone, ItemAndPreEnvContents
from dero.latex.logic.extract.filepaths import get_filepaths_from_items
from dero.latex.logic.extract.binaries import get_binaries_from_items
from dero.latex.models.references.bibtex.base import BibTexEntryBase
from dero.latex.models.control.filecontents import FileContents
from dero.latex.models.references.bibtex.addresource import AddBibResource


class DocumentEnvironment(Environment):
    name = 'document'

    def __init__(self):
        super().__init__(name=self.name)

class Document(DocumentItem, Item):
    name = 'document'

    def __init__(self, content: ItemOrListOfItems, packages: List[Package]=None, landscape=False,
                 title: str=None, author: str=None, date: str=None, abstract: str=None,
                 references: Optional[Sequence[BibTexEntryBase]] = None,
                 skip_title_page: bool=False,
                 page_modifier_str: Optional[str]='margin=0.8in, bottom=1.2in', page_header: bool=False,
                 page_numbers: bool=True, appendix_modifier_str: Optional[str] = 'page',
                 section_numbering_styles: Optional[Dict[str, str]] = None):
        from dero.latex.logic.builder import _build
        from dero.latex.models.titlepage import TitlePage

        self.has_references = references is not None

        if packages is None:
            packages = default_packages.copy()

        if page_modifier_str is not None:
            # Set margins, body size, etc. with geometry package
            packages.append(Package('geometry', modifier_str=page_modifier_str))

        if section_numbering_styles is None:
            section_numbering_styles = {}

        packages.append(Package('appendix', modifier_str=appendix_modifier_str))

        if references:
            packages.append(Package('filecontents'))
            packages.append(Package('biblatex', modifier_str='backend=bibtex,citestyle=authoryear,natbib'))

        section_num_styles = SectionNumberingFormatter.list_from_string_format_dict(section_numbering_styles)

        self.packages = packages

        possible_pre_env_contents = [
            _document_class_str(),
            *[str(package) for package in self.packages],
            *section_num_styles,
            PageStyle('fancy'),

            # header is there by default. add remove header lines if page_header=False
            remove_header if not page_header else None,

            # add right page numbers. if not, use blank center footer to clear default page numbers in center footer
            right_aligned_page_numbers if page_numbers else CenterFooter('')
        ]

        self.pre_env_contents = _build([item for item in possible_pre_env_contents if item is not None])

        if isinstance(content, (Item, str)):
            content = [content]

        if not skip_title_page and _should_create_title_page(title=title, author=author, date=date, abstract=abstract):
            title_page = TitlePage(title=title, author=author, date=date, abstract=abstract)
            content.insert(0, title_page)
            self.has_title_page = True
        else:
            self.has_title_page = False

        if references:
            use_resource = AddBibResource('refs.bib')
            self.pre_env_contents = _build([self.pre_env_contents, use_resource])
            all_references = _build(references)
            references_inline_file = FileContents(all_references, 'refs.bib')
            content.append(references_inline_file)

        self.content = content

        self.filepaths = self._get_filepaths_from_items(content)
        self.binaries = get_binaries_from_items(content)

        # combine content into a single str
        content = _build(content)

        if landscape:
            content = Landscape().wrap(str(content))

        super().__init__(self.name, content, pre_env_contents=self.pre_env_contents)

    def __repr__(self):
        return f'<Document>'

    def _repr_pdf_(self):
        tex = str(self)

        return latex_str_to_pdf_obj_with_sources(
            tex,
            image_paths=self.filepaths,
            image_binaries=self.binaries,
            run_bibtex=self.has_references
        ).readb()

    def to_pdf_and_move(self, outfolder, outname='document',
                              move_folder_name='Tables', as_document=True):
        tex = str(self)

        outname = latex_filename_replacements(outname)

        document_to_pdf_and_move(
            tex,
            outfolder=outfolder,
            outname=outname,
            image_paths=self.filepaths,
            move_folder_name=move_folder_name,
            as_document=as_document,
            image_binaries=self.binaries,
            run_bibtex=self.has_references
        )

    def _get_filepaths_from_items(self, content: ListOfItems) -> StrListOrNone:
        return get_filepaths_from_items(content)

    @classmethod
    def from_ambiguous_collection(cls, collection, **document_kwargs):
        content = extract_document_items_from_ambiguous_collection(collection)

        return cls(content, **document_kwargs)

def _should_create_title_page(title: str = None, author: str = None, date: str = None, abstract: str = None):
    return any([
        title is not None,
        author is not None,
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

