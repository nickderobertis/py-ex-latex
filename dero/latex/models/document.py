from typing import List, Union, Tuple

from dero.latex.models.environment import Environment
from dero.latex.models import Item
from dero.latex.models.documentitem import DocumentItem
from dero.latex.texgen import _document_class_str
from dero.latex.models.package import Package
from dero.latex.texgen.packages import default_packages
from dero.latex.models.page.style import PageStyle
from dero.latex.models.landscape import Landscape
from dero.latex.logic.pdf import _document_to_pdf_and_move
from dero.latex.texgen.replacements.filename import latex_filename_replacements
from dero.latex.logic.extract.docitems import extract_document_items_from_ambiguous_collection
from dero.latex.models.page.number import right_aligned_page_numbers
from dero.latex.models.page.header import remove_header
from dero.latex.models.page.footer import CenterFooter
from dero.latex.models.section.abstract import Abstract

AnyItem = Union[Item, DocumentItem]
ListOfItems = List[AnyItem]
ItemOrListOfItems = Union[AnyItem, ListOfItems]
StrList = List[str]
StrListOrNone = Union[StrList, None]
ItemAndPreEnvContents = Tuple[AnyItem, StrListOrNone]

class DocumentEnvironment(Environment):
    name = 'document'

    def __init__(self):
        super().__init__(name=self.name)

class Document(DocumentItem, Item):
    name = 'document'

    def __init__(self, content: ItemOrListOfItems, packages: List[Package]=None, landscape=False,
                 title: str=None, author: str=None, date: str=None, abstract: str=None,
                 skip_title_page: bool=False,
                 page_modifier_str: str='margin=0.8in, bottom=1.2in', page_header: bool=False,
                 page_numbers: bool=True):
        from dero.latex.logic.builder import _build
        from dero.latex.models.titlepage import TitlePage

        if packages is None:
            packages = default_packages.copy()

        # Set margins, body size, etc. with geometry package
        packages.append(Package('geometry', modifier_str=page_modifier_str))

        self.packages = packages

        possible_pre_env_contents = [
            _document_class_str(),
            *[str(package) for package in self.packages],
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

        self.filepaths = self._get_filepaths_from_items(content)

        # combine content into a single str
        content = _build(content)

        if landscape:
            content = Landscape().wrap(str(content))

        super().__init__(self.name, content, pre_env_contents=self.pre_env_contents)

    def __repr__(self):
        return f'<Document>'

    def to_pdf_and_move(self, outfolder, outname='document',
                              move_folder_name='Tables', as_document=True):
        tex = str(self)

        outname = latex_filename_replacements(outname)

        _document_to_pdf_and_move(
            tex,
            outfolder=outfolder,
            outname=outname,
            image_paths=self.filepaths,
            move_folder_name=move_folder_name,
            as_document=as_document
        )

    def _get_filepaths_from_items(self, content: ListOfItems) -> StrListOrNone:
        from dero.latex.figure import Figure

        filepaths = []
        for item in content:
            # TODO: handling for other types which may have filepaths
            if isinstance(item, Figure):
                filepaths += item.filepaths

        if filepaths == []:
            return None

        return filepaths

    @classmethod
    def from_ambiguous_collection(cls, collection, packages: List[Package]=None, landscape=False,
                                  title=None, author=None, date=None, skip_title_page: bool=False,
                                  page_modifier_str: str = 'margin=0.8in, bottom=1.2in', page_header: bool = False,
                                  page_numbers: bool = True
                                  ):
        content = extract_document_items_from_ambiguous_collection(collection)

        return cls(content, packages=packages, landscape=landscape,
                   title=title, author=author, date=date, skip_title_page=skip_title_page,
                   page_modifier_str=page_modifier_str, page_header=page_header,
                   page_numbers=page_numbers)

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

