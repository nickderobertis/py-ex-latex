from typing import List, Optional, Callable, cast

from pyexlatex.models.format.breaks import OutputLineBreak
from pyexlatex.models.format.raw import Raw
from pyexlatex.letter.closing import Closing
from pyexlatex.letter.enclosures import Enclosures
from pyexlatex.letter.letter import Letter
from pyexlatex.letter.opening import Opening
from pyexlatex.letter.ps import PS
from pyexlatex.letter.signature import Signature
from pyexlatex.models.document import DocumentBase
from pyexlatex.resume.models.contactline import ContactLine
from pyexlatex.typing import ItemOrListOfItems, PyexlatexItems, PyexlatexItem
from pyexlatex.models.package import Package
from pyexlatex.models.control.documentclass.documentclass import DocumentClass


class LetterDocument(DocumentBase):
    """
    The main high-level document class for creating letters.
    """
    name = 'document'

    def __init__(self, content: PyexlatexItems, contact_info: Optional[PyexlatexItems] = None,
                 to_contact_info: PyexlatexItems = '',
                 signer_name: Optional[PyexlatexItems] = None, closing_indent: str = '0pt',
                 salutation: PyexlatexItems = 'Dear Sir or Madam:', closing: Optional[PyexlatexItems] = 'Sincerely,',
                 ps: Optional[PyexlatexItems] = None, enclosures: Optional[PyexlatexItems] = None,
                 packages: List[Package] = None,
                 pre_env_contents: Optional[ItemOrListOfItems] = None,
                 font_size: Optional[float] = None, doc_class_options: Optional[List[str]] = None,
                 pre_output_func: Optional[Callable] = None):

        self.document_class_obj = DocumentClass(
            document_type='letter',
            font_size=font_size,
            options=doc_class_options
        )

        self.add_data_from_content(
            [content, contact_info, to_contact_info, signer_name, salutation, closing, ps, enclosures]
        )

        all_pre_env_contents: List[PyexlatexItems] = []

        if contact_info is not None:
            all_pre_env_contents.append(ContactLine(contact_info))
        if signer_name is not None:
            all_pre_env_contents.append(Signature(signer_name))
        all_pre_env_contents.append(Raw(fr'\longindentation={closing_indent}'))

        if pre_env_contents is not None:
            all_pre_env_contents.extend(pre_env_contents)

        letter_contents = [
            Opening(salutation),
            content,
        ]

        if closing is not None:
            letter_contents.append(Closing(closing))
        if ps is not None:
            letter_contents.append(PS(ps))
        if enclosures is not None:
            letter_contents.append(Enclosures(enclosures))

        if isinstance(to_contact_info, (list, tuple)):
            to_contact_info = f' {OutputLineBreak()} '.join(to_contact_info)
        to_contact_info = cast(PyexlatexItem, to_contact_info)

        letter = Letter(modifiers=self._wrap_with_braces(to_contact_info)).wrap(letter_contents)

        super().__init__(
            letter,
            packages=packages,
            pre_env_contents=all_pre_env_contents,  # type: ignore
            pre_output_func=pre_output_func,
        )


