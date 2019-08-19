from dero.latex.models.mixins import IsSpecificClassMixin
from dero.latex.models.item import IsLatexItemMixin


class DocumentItem(IsSpecificClassMixin, IsLatexItemMixin):
    """
    Used for differentiating which items can be directly included in a document
    """
    is_DocumentItem = True
