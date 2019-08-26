from pyexlatex.models.format.code.minted import Minted


class Python(Minted):
    """
    Renders passed contents as Python code, with syntax highlighting.
    """

    def __init__(self, contents):
        super().__init__(contents, 'python')
