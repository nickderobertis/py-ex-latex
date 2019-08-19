from pyexlatex.models.item import SimpleItem


class End(SimpleItem):
    name = 'end'

    def __init__(self, env: str):
        self.env = env
        super().__init__(self.name, env)
