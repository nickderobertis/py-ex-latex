from pyexlatex.models.template import Template
from pyexlatex.models.control.newcounter import NewCounter
from pyexlatex.models.control.setcounter import SetCounter
from pyexlatex.models.control.value import Value
from pyexlatex.models.item import NoOptionsNoContentsItem


class _Appendix(NoOptionsNoContentsItem):
    name = 'appendix'

    def __init__(self, **kwargs):
        super().__init__(self.name, **kwargs)


class PresentationAppendix(Template):
    """
    Appendix to be used in a beamer presentation
    """

    def __init__(self, content):
        if not isinstance(content, (list, tuple)):
            content = [content]
        self.content = content
        self.contents = self._get_contents()
        super().__init__()

    def _get_contents(self):
        pre_content_contents = [
            NewCounter('finalframe'),
            SetCounter('finalframe', Value('framenumber'))
        ]

        post_content_contents = [
            SetCounter('framenumber', Value('finalframe'))
        ]

        return [
            _Appendix(),
            *pre_content_contents,
            *self.content,
            *post_content_contents
        ]