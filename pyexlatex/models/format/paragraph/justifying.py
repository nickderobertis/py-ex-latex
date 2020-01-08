from pyexlatex.models.item import NoOptionsNoContentsItem


class Justifying(NoOptionsNoContentsItem):
    """
    Returns paragraph to the default of justifying text on both left and right. Useful if paragraph is currently
    ragged or sloppy, which occurs when using NoLineBreak.
    """
    name = 'justifying'

    def __init__(self, **kwargs):
        self.add_package('ragged2e')
        super().__init__(self.name, **kwargs)