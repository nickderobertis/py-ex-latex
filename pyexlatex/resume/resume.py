from typing import List, Optional, Sequence, Union, Callable
from pyexlatex.models.document import DocumentBase
from pyexlatex.typing import ItemOrListOfItems
from pyexlatex.models.package import Package
from pyexlatex.models.control.documentclass.documentclass import DocumentClass
from pyexlatex.resume.models.name import Name
from pyexlatex.resume.models.contactline import ContactLine


class Resume(DocumentBase):
    """
    The main high-level class for creating resumes
    """
    name = 'document'

    def __init__(self, content: ItemOrListOfItems, packages: List[Package]=None,
                 pre_env_contents: Optional[ItemOrListOfItems] = None,
                 name: Optional[str] = None, contact_lines: Optional[Sequence[Union[str, Sequence[str]]]] = None,
                 font_size: Optional[float] = 11,
                 page_modifier_str: Optional[str]='left=0.75in,top=0.6in,right=0.75in,bottom=0.6in',
                 authors: Optional[Union[str, Sequence[str]]] = None, pre_output_func: Optional[Callable] = None):

        self.init_data()

        self.document_class_obj = DocumentClass(
            document_type='resume',
            font_size=font_size,
        )

        from pyexlatex.models.item import ItemBase
        if pre_env_contents is None:
            pre_env_contents_list = []
        elif isinstance(pre_env_contents, (ItemBase, str)):
            pre_env_contents_list = [pre_env_contents]
        else:
            pre_env_contents_list = pre_env_contents  # type: ignore

        name = self._get_name(name, authors)

        if name is not None:
            pre_env_contents_list.append(
                Name(name)
            )

        if contact_lines is not None:
            pre_env_contents_list.extend(
                [ContactLine(contact_info) for contact_info in contact_lines]
            )

        if page_modifier_str is not None:
            # Set margins, body size, etc. with geometry package
            self.data.packages.append(Package('geometry', modifier_str=page_modifier_str))

        super().__init__(
            content,
            packages=packages,
            pre_env_contents=pre_env_contents_list,
            pre_output_func=pre_output_func,
        )

    def _get_name(self, name: Optional[str] = None, authors: Optional[Union[str, Sequence[str]]] = None):
        if authors is None:
            return name
        elif name is None:
            # Authors is passed, name is not
            if isinstance(authors, (list, tuple)):
                authors = authors[0]
            return authors

        # Both name and author passed

        if name == authors:
            return name

        # Name and author are not the same
        raise ValueError(f'got different name and authors, not clear which to use. name: {name}, authors: {authors}')

