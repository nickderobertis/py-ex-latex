from typing import Optional
import pyexlatex as pl


class SpacedSection(pl.Template):
    """
    A section which appropriately spaces content for a resume.
    """

    def __init__(self, contents, title: Optional[str] = None, break_adjustment: str = '-6pt',
                 end_adjustment: str = '-20pt'):
        if not isinstance(contents, (list, tuple)):
            contents = [contents]

        all_contents = []
        for content in contents:
            all_contents.append(content)
            all_contents.append('')
            # all_contents.append(pl.OutputLineBreak(size_adjustment=break_adjustment))
        all_contents[-1] = pl.OutputLineBreak(size_adjustment=end_adjustment)  # replace final spacing

        self.contents = pl.Section(all_contents, title=title)
        super().__init__()
