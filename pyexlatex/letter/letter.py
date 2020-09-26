from pyexlatex.models.section.base import EnvironmentTextArea


class Letter(EnvironmentTextArea):
    name = 'letter'

    def __init__(self, **kwargs):
        super().__init__(name=self.name, **kwargs)
