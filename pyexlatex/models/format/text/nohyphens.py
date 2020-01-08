from pyexlatex.models.item import SimpleItem


class NoHyphens(SimpleItem):
    """
    Prevents a line break within text, where a hyphen would normally be placed. However when it is used alone it
    will make text run over the margin. Use NoLineBreak to avoid this.
    """
    name = 'nohyphens'

    def __init__(self, contents, **kwargs):
        self.init_data()
        self.data.packages.append('hyphenat')
        super().__init__(self.name, contents, **kwargs)
