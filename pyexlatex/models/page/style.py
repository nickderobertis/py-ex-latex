from pyexlatex.models.item import SimpleItem


class PageStyle(SimpleItem):
    """
    Sets style of the pages for the entire document.
    """
    name = 'pagestyle'

    def __init__(self, contents):
        super().__init__(self.name, contents)


class ThisPageStyle(SimpleItem):
    """
    Sets style of the current page in a document.
    """
    name = 'thispagestyle'

    def __init__(self, contents):
        super().__init__(self.name, contents)