
class Environment:

    def __init__(self, name):
        self.name = name

        self._begin = _begin_str(name)
        self._end = _end_str(name)

    def __repr__(self):
        return f'<Environment(name={self.name})>'

    def wrap(self, other):
        return '\n'.join([self._begin, other, self._end])


def _begin_str(str_):
    return rf'\begin{{{str_}}}'

def _end_str(str_):
    return fr'\end{{{str_}}}'