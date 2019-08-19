class StringAdditionMixin:

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)

    def join(self, iterable):
        return self.__str__().join(str(i) for i in iterable)


class StringEqMixin:

    def __eq__(self, value):
        return str(self) == str(value)

    def __hash__(self):
        return hash(str(self))


class IsSpecificClassMixin:
    """
    creates attribute is_ClassName (with whatever class name)

    be sure to put this mixin first among multiple classes
    """

    def __init__(self, *args, **kwargs):
        class_name = self.__class__.__name__
        setattr(self, f'is_{class_name}', True)
        super().__init__(*args, **kwargs)
