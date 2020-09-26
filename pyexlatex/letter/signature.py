from pyexlatex.models.item import SimpleItem
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.typing import PyexlatexItems


class Signature(TextAreaMixin, SimpleItem):
    name = 'signature'

    def __init__(self, signer: PyexlatexItems):
        self.signer = signer
        super().__init__(self.name, self.signer)
