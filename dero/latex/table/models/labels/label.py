from dero.latex.models.mixins import ReprMixin


class Label(ReprMixin):
    repr_cols = ['value']

    def __init__(self, value):
        pass