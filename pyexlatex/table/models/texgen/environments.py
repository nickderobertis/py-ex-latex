from pyexlatex.models.environment import Environment

class TableEnvironment(Environment):
    name = 'table'

    def __init__(self):
        super().__init__(name=self.name)

class ThreePartTableEnvironment(Environment):
    name = 'threeparttable'

    def __init__(self):
        super().__init__(name=self.name)

class TabularEnvironment(Environment):
    name = 'tabular'

    def __init__(self):
        super().__init__(name=self.name)
