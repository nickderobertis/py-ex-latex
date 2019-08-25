from pyexlatex.models.format.code.minted import Minted


class Python(Minted):

    def __init__(self, contents):
        super().__init__(contents, 'python')
