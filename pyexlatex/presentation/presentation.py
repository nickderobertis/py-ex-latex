from typing import List, Optional, Sequence, Union, TYPE_CHECKING, Callable

from pyexlatex.presentation.beamer.control.navigation import AddNavigationHeader
from pyexlatex.presentation.beamer.templates.control.tocsection import TableOfContentsAtBeginSection

if TYPE_CHECKING:
    from pyexlatex.models.documentsetup import DocumentSetupData
from copy import deepcopy
from pyexlatex.models.document import DocumentBase
from pyexlatex.typing import ItemOrListOfItems, PyexlatexItems
from pyexlatex.models.package import Package
from pyexlatex.models.control.documentclass.documentclass import DocumentClass
from pyexlatex.models.control.mode import Mode
from pyexlatex.presentation.beamer.theme.usetheme import UseTheme
from pyexlatex.models.title.frame import TitleFrame, should_create_title_frame
from pyexlatex.models.item import ItemBase, Item
from pyexlatex.presentation.beamer.templates.lists.dim_reveal_items import eliminate_dim_reveal
from pyexlatex.exc import NoPackageWithNameException


class Presentation(DocumentBase):
    """
    The main high-level class for creating presentations, can render presentations as PDF in either a presenter
    style or a handouts style.
    """
    name = 'document'

    def __init__(self, content: PyexlatexItems, packages: List[Union[Package, str]] = None,
                 pre_env_contents: Optional[PyexlatexItems] = None,
                 title: Optional[str] = None, authors: Optional[Union[str, Sequence[str]]] = None,
                 date: Optional[str] = None,
                 short_title: Optional[str] = None, subtitle: Optional[str] = None, short_author: Optional[str] = None,
                 institutions: Optional[Sequence[Sequence[str]]] = None, short_institution: Optional[str] = None,
                 font_size: Optional[float] = 11, theme: str = 'Madrid', backend: str = 'beamer',
                 nav_header: bool = False, toc_sections: bool = False, handouts: bool = False,
                 pre_output_func: Optional[Callable] = None):

        self.init_data()
        self.title_frame = None

        from pyexlatex.models.documentitem import DocumentItem
        content_list: List[Union[Item, ItemBase, str]]
        if isinstance(content, (ItemBase, str)):
            content_list = [content]
        else:
            # don't overwrite existing content
            content_list = deepcopy(content)  # type: ignore

        pre_env_contents_list: List[Union[Item, ItemBase, str]]
        if pre_env_contents is None:
            pre_env_contents_list = []
        elif isinstance(pre_env_contents, (ItemBase, str)):
            pre_env_contents_list = [pre_env_contents]
        else:
            pre_env_contents_list = pre_env_contents  # type: ignore

        if backend != 'beamer':
            raise NotImplementedError('only beamer backend is currently supported for Presentation')

        doc_class_options: Optional[List[str]]
        if handouts:
            doc_class_options = ['handout']
            elimate_overlays(content_list)
            eliminate_dim_reveal(content_list)
        else:
            doc_class_options = None

        self.document_class_obj = DocumentClass(
            document_type=backend,
            font_size=font_size,
            options=doc_class_options
        )

        data_cleanup_func: Optional[Callable[[DocumentSetupData], None]]
        if backend == 'beamer':
            # Remove hyperref package if added, as may conflict with beamer which already loads it
            def remove_hyperref(data: 'DocumentSetupData') -> None:
                try:
                    data.packages.delete_by_name('hyperref')
                except NoPackageWithNameException:
                    pass
            data_cleanup_func = remove_hyperref

            # TODO [#17]: add support for custom presentation theming, not just passing main theme str
            styles = [UseTheme(theme)]
            self.data.packages.append(
                Mode(
                    mode_type='presentation',
                    contents=styles
                )
            )

            if should_create_title_frame(title, authors, date, subtitle, institutions):
                self.title_frame = TitleFrame(
                    title=title,
                    authors=authors,
                    date=date,
                    short_title=short_title,
                    subtitle=subtitle,
                    short_author=short_author,
                    institutions=institutions,
                    short_institution=short_institution
                )
                content_list.insert(0, self.title_frame)

            if nav_header:
                pre_env_contents_list.append(AddNavigationHeader())

            if toc_sections:
                pre_env_contents_list.append(TableOfContentsAtBeginSection())

        else:
            data_cleanup_func = None

        super().__init__(
            content_list,
            packages=packages,
            pre_env_contents=pre_env_contents_list,
            data_cleanup_func=data_cleanup_func,
            pre_output_func=pre_output_func
        )


def elimate_overlays(content):
    """
    Eliminates overlays from nested content. Modifies in place
    """
    if hasattr(content, 'content'):
        elimate_overlays(content.content)
    if hasattr(content, 'contents'):
        elimate_overlays(content.contents)
    if hasattr(content, 'overlay'):
        content.overlay = None
    if isinstance(content, (list, tuple)):
        [elimate_overlays(c) for c in content]

