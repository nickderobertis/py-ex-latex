from typing import Union
from pyexlatex.models.template import Template
from pyexlatex.models.format.fills import VFill, HFill


class SpacedBase(Template):
    """
    Base class for VerticallySpaced and HorizontallySpaced. Handles the logic of adding VFill and HFill between and
    around items.
    """

    def __init__(self, content, vertically_space: bool, pad_ends: bool):
        self.orig_content = content
        self.vertically_space = vertically_space
        self.pad_ends = pad_ends
        self.contents = self._get_contents()
        super().__init__()

    def _get_contents(self):
        if not isinstance(self.orig_content, (list, tuple)):
            orig_content = [self.orig_content]
        else:
            orig_content = self.orig_content

        orig_valid_content = [item for item in orig_content if item is not None]

        contents = []
        for content in orig_valid_content:
            contents.extend([
                content,
                self.spacer
            ])
        del contents[-1]  # strip final spacer

        if self.pad_ends:
            # Add additional spacers at beginning and end
            contents.insert(0, self.spacer)
            contents.append(self.spacer)

        return contents


    @property
    def spacer(self) -> Union[VFill, HFill]:
        if self.vertically_space:
            return VFill()
        return HFill()


class VerticallySpaced(SpacedBase):
    """
    Inserts vertical spacing between items until they fill the content area
    """

    def __init__(self, content, pad_ends: bool = False):
        """

        :param content:
        :param pad_ends: whether to add spacing outside the content as well
        """
        super().__init__(content, vertically_space=True, pad_ends=pad_ends)


class HorizontallySpaced(SpacedBase):
    """
    Inserts horiztonal spacing between items until they fill the content area
    """

    def __init__(self, content, pad_ends: bool = False):
        """

        :param content:
        :param pad_ends: whether to add spacing outside the content as well
        """
        super().__init__(content, vertically_space=False, pad_ends=pad_ends)
