from pyexlatex.models.item import NoOptionsNoContentsItem


class PageBreak(NoOptionsNoContentsItem):
    """
    Adds a break point where a new page should be started.
    """
    name = 'newpage'

    def __init__(self):
        super().__init__(self.name)
