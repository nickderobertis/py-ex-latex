from pyexlatex.models.item import Item
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.models.commands.newenvironment import NewEnvironment


class EnvironmentTemplate(TextAreaMixin, Item):
    """
    Base class which makes it easy to create new environment types.

    Examples:
    >>> import pyexlatex as pl
    >>> class BoldEnvironment(pl.EnvironmentTemplate):
    >>>     name = 'myenv'
    >>>     begin_def = r'\bf'
    >>>     end_def = ''
    >>>
    >>> print(pl.Document(BoldEnvironment('woo')))
    \documentclass[]{article}
    \newenvironment{myenv}{\bf}{}
    ...
    \begin{document}
    \begin{myenv}
    woo
    \end{myenv}
    \end{document}


    """
    begin_def = ''
    end_def = ''

    def __init__(self, contents, **kwargs):
        self.init_data()
        self.data.begin_document_items.append(self._environment_def)
        super().__init__(self.name, contents, **kwargs)

    @property
    def _environment_def(self) -> NewEnvironment:
        return NewEnvironment(
            self.name,
            self.begin_def,
            self.end_def
        )
