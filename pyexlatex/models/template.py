from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.models.item import ItemBase


class Template(TextAreaMixin, ItemBase):
    r"""
    Base class for creating custom Pyexlatex templates.

    To use, simply subclass Template, then in __init__, set the attribute .contents, and call super().__init__().
    The .contents attribute should be set to a string, pyexlatex object, or iterable of those.

    Examples:

    Contents can be a Pyexlatex object or string:

    >>> import pyexlatex as pl
    >>> class BoldUnderline(pl.Template):
    >>>
    >>>     def __init__(self, contents):
    >>>         self.contents = pl.Bold(pl.Underline(contents))
    >>>         super().__init__()
    >>>
    >>> print(BoldUnderline('woo'))
    \textbf{\underline{woo}}

    Contents can also be an iterable of strings or Pyexlatex objects

    >>> import pyexlatex as pl
    >>> class BoldAndUnderline(pl.Template):
    >>>
    >>>     def __init__(self, bold_contents, underline_contents, *other_contents):
    >>>         self.contents = [
    >>>             pl.Bold(bold_contents),
    >>>             pl.Underline(underline_contents),
    >>>             *other_contents
    >>>         ]
    >>>         super().__init__()
    >>>
    >>> print(BoldAndUnderline('woo bold', 'woo underline', 'something'))
    \textbf{woo bold}
    \underline{woo underline}
    something

    """

    def __init__(self):
        self._validate_contents()
        super().__init__(None, self.contents)

    def __str__(self):
        if isinstance(self.contents, str):
            return self.contents
        elif hasattr(self.contents, 'is_LatexItem') and self.contents.is_LatexItem:
            # Another pyexlatex item is the root contents, allow it to determine str output
            return str(self.contents)
        else:
            # An iterable of pyexlatex items
            from pyexlatex.logic.builder import _build
            return _build(self.contents)

    def _validate_contents(self):
        contents_exception = ContentParseException(
            f'not able to parse attribute .contents in {self.__class__.__name__}. '
            f'Ensure that .contents is set to a string, a pyexlatex item, or '
            f'an iterable. Got {self.contents} of type {type(self.contents)}.'
        )

        if isinstance(self.contents, str):
            return
        elif hasattr(self.contents, 'is_LatexItem') and self.contents.is_LatexItem:
            return
        elif isinstance(self.contents, dict):
            raise contents_exception
        else:
            try:
                from pyexlatex.logic.builder import _build
                _build(self.contents)
            except TypeError as e:
                if 'can only join an iterable' in e:
                    raise contents_exception



class ContentParseException(Exception):
    pass

