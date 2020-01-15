from typing import Optional, Any, Sequence
from pyexlatex.models.item import MultiOptionSimpleItem
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.models.package import Package
from pyexlatex.exc import NoPackageWithNameException


class Hyperlink(TextAreaMixin, MultiOptionSimpleItem):
    """
    Create links to urls, with or without displaying text instead of the link.
    """

    def __init__(self, href: str, content: Optional[Any] = None, **kwargs):
        self.href = href
        self.content = content

        options: Sequence[Any]
        if content is None:
            self.name = 'url'
            options = (href,)
        else:
            self.name = 'href'
            options = (href, content)

        self.add_data_from_content(content)
        self.data.packages.append(
            # TODO [#14]: Figure out way to have different options for different hyperlinks
            #
            # Think about passing options. Difficult because mutliple Hyperlinks could be constructed with
            # different options, then not clear which to take.
            Package('hyperref', modifier_str='hidelinks')
        )

        MultiOptionSimpleItem.__init__(self, self.name, *options, **kwargs)
