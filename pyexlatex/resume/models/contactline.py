from typing import Sequence, Union
from pyexlatex.models.item import SimpleItem
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.models.format.breaks import OutputLineBreak


class ContactLine(TextAreaMixin, SimpleItem):
    name = 'address'

    def __init__(self, contact_info: Union[str, Sequence[str]]):
        self.contact_info = contact_info
        self.add_data_from_content(contact_info)

        super().__init__(self.name, self._get_content())

    def _get_content(self):
        if isinstance(self.contact_info, str):
            return self.contact_info

        separator = f' {OutputLineBreak()} '
        return separator.join([str(item) for item in self.contact_info])
