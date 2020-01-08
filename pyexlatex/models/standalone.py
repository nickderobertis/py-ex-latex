from typing import List, Optional, Sequence, Callable
from pyexlatex.models.document import DocumentBase
from pyexlatex.typing import ItemOrListOfItems
from pyexlatex.models.package import Package
from pyexlatex.models.control.documentclass.documentclass import DocumentClass


class Standalone(DocumentBase):
    """
    The main high-level class for creating one-off graphics, equations, etc. Does not provide any document structure
    and will crop the document to the contents.
    """
    name = 'document'

    def __init__(self, content: ItemOrListOfItems, packages: List[Package] = None,
                 pre_env_contents: Optional[ItemOrListOfItems] = None,
                 font_size: Optional[float] = None, doc_class_options: Optional[List[str]] = None,
                 pre_output_func: Optional[Callable] = None):

        self.document_class_obj = DocumentClass(
            document_type='standalone',
            font_size=font_size,
            options=doc_class_options
        )

        super().__init__(
            content,
            packages=packages,
            pre_env_contents=pre_env_contents,
            pre_output_func=pre_output_func,
        )


