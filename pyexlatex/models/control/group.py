from pyexlatex.models.template import Template


class Group(Template):
    """
    Groups together latex items so that "global" commands will only affect the items in a group
    """

    def __init__(self, contents):
        if not isinstance(contents, (list, tuple)):
            contents = [contents]
        contents.insert(0, '{')
        contents.append('}')
        self.contents = contents
        super().__init__()
