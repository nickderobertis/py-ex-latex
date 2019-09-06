from typing import List, Optional, Sequence, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.models.documentsetup import DocumentSetupData
from copy import deepcopy
from pyexlatex.models.document import DocumentBase
from pyexlatex.typing import ItemOrListOfItems
from pyexlatex.models.package import Package
from pyexlatex.models.control.documentclass.documentclass import DocumentClass
from pyexlatex.models.control.mode import Mode
from pyexlatex.presentation.beamer.theme.usetheme import UseTheme
from pyexlatex.models.title.frame import TitleFrame, should_create_title_frame
from pyexlatex.models.item import ItemBase
from pyexlatex.presentation.beamer.templates.lists.dim_reveal_items import eliminate_dim_reveal
from pyexlatex.exc import NoPackageWithNameException


class Presentation(DocumentBase):
    """
    The main high-level class for creating presentations, can render presentations as PDF in either a presenter
    style or a handouts style.
    """
    name = 'document'

    def __init__(self, content: ItemOrListOfItems, packages: List[Package]=None,
                 pre_env_contents: Optional[ItemOrListOfItems] = None,
                 title: Optional[str] = None, authors: Optional[Union[str, Sequence[str]]] = None,
                 date: Optional[str] = None,
                 short_title: Optional[str] = None, subtitle: Optional[str] = None, short_author: Optional[str] = None,
                 institutions: Optional[Sequence[Sequence[str]]] = None, short_institution: Optional[str] = None,
                 font_size: Optional[float] = 11, theme: str = 'Madrid', backend: str = 'beamer',
                 handouts: bool = False):

        self.init_data()
        self.title_frame = None

        if isinstance(content, (ItemBase, str)):
            content = [content]
        else:
            content = deepcopy(content)  # don't overwrite existing content

        if backend != 'beamer':
            raise NotImplementedError('only beamer backend is currently supported for Presentation')

        if handouts:
            doc_class_options = ['handout']
            elimate_overlays(content)
            eliminate_dim_reveal(content)
        else:
            doc_class_options = None

        self.document_class_obj = DocumentClass(
            document_type=backend,
            font_size=font_size,
            options=doc_class_options
        )

        if backend == 'beamer':
            # Remove hyperref package if added, as may conflict with beamer which already loads it
            def remove_hyperref(data: 'DocumentSetupData') -> None:
                try:
                    data.packages.delete_by_name('hyperref')
                except NoPackageWithNameException:
                    pass
            data_cleanup_func = remove_hyperref

            # TODO: add support for custom theming, not just passing main theme str
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
                content.insert(0, self.title_frame)
        else:
            data_cleanup_func = None

        super().__init__(
            content,
            packages=packages,
            pre_env_contents=pre_env_contents,
            data_cleanup_func=data_cleanup_func
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

