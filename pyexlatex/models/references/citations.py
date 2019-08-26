from pyexlatex.models.item import SimpleItem
from pyexlatex.models.package import Package


class Cite(SimpleItem):
    """
    Basic citation command, creates a reference to a document included in the bibliography.
    """
    name = 'cite'

    def __init__(self, item_accessor: str):
        super().__init__(self.name, item_accessor)


class NatBibCiteBase(Cite):

    def __init__(self, item_accessor):
        self.init_data()
        self.data.packages.append(Package('natbib'))
        return super().__init__(item_accessor)


class CiteT(NatBibCiteBase):
    """
    In text citation command, creates an in text (without parentheses) reference to a document
    included in the bibliography.
    """
    name = 'citet'


class CiteP(NatBibCiteBase):
    """
    Paragraph citation command, creates a paragraph (with parentheses) reference to a document
    included in the bibliography.
    """
    name = 'citep'
