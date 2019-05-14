from dero.latex.models.mixins import StringAdditionMixin, IsSpecificClassMixin
from dero.latex.texgen import _basic_item_str, _multi_option_item_str, _no_braces_item_str, item_equals_str


class IsLatexItemMixin:
    is_LatexItem = True


class Item(IsSpecificClassMixin, IsLatexItemMixin, StringAdditionMixin):

    def __init__(self, name, contents, pre_env_contents=None, post_env_contents=None, env_modifiers=None):
        from dero.latex.models import Environment
        self.env = Environment(name, modifiers=env_modifiers)
        self.contents = contents

        self._output = ''
        if pre_env_contents:
            self._output += pre_env_contents
        self._output += self.env.wrap(str(self.contents))
        if post_env_contents:
            self._output += post_env_contents
        super().__init__()

    def __repr__(self):
        return f'<Item(name={self.env.name}, contents={self.contents})>'

    def __str__(self):
        return self._output


class SimpleItem(IsSpecificClassMixin, IsLatexItemMixin, StringAdditionMixin):

    def __init__(self, name, contents):
        self.name = name
        self.contents = contents
        super().__init__()

    def __repr__(self):
        return f'<{self.name.title()}({self.contents})>'

    def __str__(self):
        return _basic_item_str(self.name, self.contents)


class MultiOptionSimpleItem(IsSpecificClassMixin, IsLatexItemMixin, StringAdditionMixin):

    def __init__(self, name, *options):
        self.name = name
        self.options = options
        super().__init__()

    def __repr__(self):
        return f'<{self.name.title()}({self.options})>'

    def __str__(self):
        return _multi_option_item_str(self.name, *self.options)


class NoBracesItem(IsSpecificClassMixin, IsLatexItemMixin, StringAdditionMixin):

    def __init__(self, name, contents):
        self.name = name
        self.contents = contents
        super().__init__()

    def __repr__(self):
        return f'<{self.name.title()}({self.contents})>'

    def __str__(self):
        return _no_braces_item_str(self.name, self.contents)


class EqualsItem(IsSpecificClassMixin, IsLatexItemMixin, StringAdditionMixin):

    def __init__(self, name, contents):
        self.name = name
        self.contents = contents
        super().__init__()

    def __repr__(self):
        return f'<{self.name.title()}({self.contents})>'

    def __str__(self):
        return item_equals_str(self.name, self.contents)
