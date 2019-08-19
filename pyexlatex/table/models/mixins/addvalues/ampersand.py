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