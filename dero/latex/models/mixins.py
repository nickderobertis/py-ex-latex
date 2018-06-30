class StringAdditionMixin:

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)

    def join(self, iterable):
        return self.__str__().join(str(i) for i in iterable)


