from dero.latex.table.models.table.row import Row


class AmpersandAddMixin:

    def __add__(self, other):
        if hasattr(self, 'value') and hasattr(other, 'value'):
            return self.value + ' & ' + other.value
        elif hasattr(self, 'values') and hasattr(other, 'value'):
            return ' & '.join(self.values + [other.value])
        elif hasattr(self, 'values') and hasattr(other, 'values'):
            return ' & '.join(self.values + other.values)
        elif hasattr(self, 'value') and hasattr(other, 'values'):
            return ' & '.join([self.value] + other.values)
        elif hasattr(self, 'value'):
            return self.value + ' & ' + other
        elif hasattr(self, 'values'):
            return ' & '.join(self.values + [other])
        return self + ' & ' + other

    def __radd__(self, other):
        if hasattr(self, 'value') and hasattr(other, 'value'):
            return other.value + ' & ' + self.value
        elif hasattr(self, 'values') and hasattr(other, 'value'):
            return ' & '.join([other.value] + self.values)
        elif hasattr(self, 'values') and hasattr(other, 'values'):
            return ' & '.join(other.values + self.values)
        elif hasattr(self, 'value') and hasattr(other, 'values'):
            return ' & '.join(other.values + [self.value])
        elif hasattr(self, 'value'):
            return other + self.value + ' & '
        elif hasattr(self, 'values'):
            return ' & '.join([other] + self.values)
        return other + ' & ' + self

class RowAddMixin:

    def __add__(self, other):

        klass = self._add_class(other)

        if hasattr(self, 'value') and hasattr(other, 'value'):
            return klass([self.value, other.value])
        elif hasattr(self, 'values') and hasattr(other, 'value'):
            return klass(self.values + [other.value])
        elif hasattr(self, 'values') and hasattr(other, 'values'):
            return klass(self.values + other.values)
        elif hasattr(self, 'value') and hasattr(other, 'values'):
            return klass([self.value] + other.values)
        elif hasattr(self, 'value'):
            return klass([self.value, other])
        elif hasattr(self, 'values'):
            return klass(self.values + [other])
        return klass([self, other])

    def __radd__(self, other):
        klass = self._add_class(other)

        if hasattr(self, 'value') and hasattr(other, 'value'):
            return klass([other.value, self.value])
        elif hasattr(self, 'values') and hasattr(other, 'value'):
            return klass([other.value] + self.values)
        elif hasattr(self, 'values') and hasattr(other, 'values'):
            return klass(other.values + self.values)
        elif hasattr(self, 'value') and hasattr(other, 'values'):
            return klass(other.values + [self.value])
        elif hasattr(self, 'value'):
            return klass([other, self.value])
        elif hasattr(self, 'values'):
            return klass([other] + self.values)
        return klass([self, other])

    def _add_class(self, other):
        # keep same class if both are same class
        # otherwise, default to Row class
        self_class = type(self)
        other_class = type(other)
        klass = self_class if self_class == other_class else Row

        return klass