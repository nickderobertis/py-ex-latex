from typing import List, Optional
from dero.latex.models.document import DocumentBase
from dero.latex.typing import ItemOrListOfItems
from dero.latex.models.package import Package
from dero.latex.models.control.documentclass import DocumentClass
from dero.latex.models.control.mode import Mode
from dero.latex.models.presentation.beamer.theme.usetheme import UseTheme


class Presentation(DocumentBase):
    name = 'document'

    def __init__(self, content: ItemOrListOfItems, packages: List[Package]=None,
                 pre_env_contents: Optional[ItemOrListOfItems] = None, font_size: Optional[float] = 11,
                 theme: str = 'Madrid',
                 backend: str = 'beamer'):

        self.init_data()

        if backend != 'beamer':
            raise NotImplementedError('only beamer backend is currently supported for Presentation')

        self.document_class_obj = DocumentClass(
            document_type=backend,
            font_size=font_size
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

        super().__init__(content, packages=packages, pre_env_contents=pre_env_contents)