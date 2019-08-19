from pyexlatex.models.mixins import IsSpecificClassMixin
from pyexlatex.models.item import IsLatexItemMixin


class DocumentItem(IsSpecificClassMixin, IsLatexItemMixin):
    """
    Used for differentiating which items can be directly included in a document
    """
    is_DocumentItem = True
