from dero.latex.texgen import _toprule_str, _midrule_str, _bottomrule_str
from dero.latex.models.mixins import StringAdditionMixin, ReprMixin


class TableLine(StringAdditionMixin, ReprMixin):

    def __init__(self):
        pass

class TopRule(TableLine):

    def __str__(self):
        return _toprule_str()


class MidRule(TableLine):

    def __str__(self):
        return _midrule_str()

class BottomRule(TableLine):

    def __str__(self):
        return _bottomrule_str()