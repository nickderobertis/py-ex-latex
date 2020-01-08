from pyexlatex.models.item import SimpleItem, NoOptionsNoContentsItem
from pyexlatex.models.page.footer import RightFooter, CenterFooter
from pyexlatex.logic.builder import _build


class PageReference(SimpleItem):
    name = 'pageref'

    def __init__(self, contents):
        super().__init__(self.name, contents)


class ThisPageNumber(NoOptionsNoContentsItem):
    """
    Gets a reference to the current page number, can be included in headers and more.
    """
    name = 'thepage'

    def __init__(self):
        super().__init__(self.name)


last_page = PageReference('LastPage')
this_page = r'\thepage\ '  # TODO: use ThisPageNumber
page_reference_str = f'Page {this_page} of {last_page}'
right_aligned_page_numbers = _build([
    RightFooter(page_reference_str),  # add page number to bottom right
    CenterFooter('')  # cancel original page number at bottom center
])

