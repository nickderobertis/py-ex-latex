
class StringAdditionMixin:

    def __add__(self, other):
        return str(self) + str(other)