
class AmpersandAddMixin:

    def __add__(self, other):
        return self + ' & ' + other

    def __radd__(self, other):
        return other + ' & ' + self