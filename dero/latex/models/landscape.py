from dero.latex.models.environment import Environment

class Landscape(Environment):
    name = 'landscape'

    def __init__(self):
        super().__init__(name=self.name)