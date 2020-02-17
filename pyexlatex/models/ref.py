from pyexlatex.models.item import SimpleItem
from pyexlatex.models.label import Label


class Ref(SimpleItem):
    """
    Pass a label to create an in text reference to that label. Will display the number of the section in the text.
    """
    name = 'ref'

    def __init__(self, contents):
        if isinstance(contents, Label):
            # Get string out of label object
            contents = contents.contents
        super().__init__(self.name, contents)


class NameRef(SimpleItem):
    """
    Pass a label to create an in text reference to that label. Will display the name of the section in the text.
    """
    name = 'nameref'

    def __init__(self, contents):
        self.add_package('nameref')
        super().__init__(self.name, contents)
