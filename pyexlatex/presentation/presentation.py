from typing import List, Optional, Sequence
from copy import deepcopy
from pyexlatex.models.document import DocumentBase
from pyexlatex.typing import ItemOrListOfItems
from pyexlatex.models.package import Package
from pyexlatex.models.control.documentclass import DocumentClass
from pyexlatex.models.control.mode import Mode
from pyexlatex.presentation.beamer import UseTheme
from pyexlatex.models.title.frame import TitleFrame, should_create_title_frame
from pyexlatex.models.item import ItemBase
from pyexlatex.presentation.beamer import eliminate_dim_reveal


class Presentation(DocumentBase):
    name = 'document'

    def __init__(self, content: ItemOrListOfItems, packages: List[Package]=None,
                 pre_env_contents: Optional[ItemOrListOfItems] = None,
                 title: Optional[str] = None, author: Optional[str] = None, date: Optional[str] = None,
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
            # TODO: add support for custom theming, not just passing main theme str
            styles = [UseTheme(theme)]
            self.data.packages.append(
                Mode(
                    mode_type='presentation',
                    contents=styles
                )
            )

            if should_create_title_frame(title, author, date, subtitle, institutions):
                self.title_frame = TitleFrame(
                    title=title,
                    author=author,
                    date=date,
                    short_title=short_title,
                    subtitle=subtitle,
                    short_author=short_author,
                    institutions=institutions,
                    short_institution=short_institution
                )
                content.insert(0, self.title_frame)

        super().__init__(content, packages=packages, pre_env_contents=pre_env_contents)


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

