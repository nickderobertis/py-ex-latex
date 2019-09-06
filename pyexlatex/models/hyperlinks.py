from typing import Optional
from pyexlatex.models.item import MultiOptionSimpleItem
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.models.package import Package


class Hyperlink(TextAreaMixin, MultiOptionSimpleItem):
    """
    Create links to urls, with or without displaying text instead of the link.
    """

    def __init__(self, href: str, content: Optional = None, **kwargs):
        self.href = href
        self.content = content

        if content is None:
            self.name = 'url'
            options = (href,)
        else:
            self.name = 'href'
            options = (href, content)

        self.add_data_from_content(content)
        self.data.packages.append(
            # TODO: determine how to pass option hidelinks and also use beamer at the same time. Getting an option clash
            # TODO: error.
            Package('hyperref', modifier_str='hidelinks')
        )

        MultiOptionSimpleItem.__init__(self, self.name, *options, **kwargs)