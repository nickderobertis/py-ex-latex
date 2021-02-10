from typing import Optional

from mixins import EqHashMixin

from pyexlatex.texgen import _usepackage_str, _requirepackage_str
from pyexlatex.models.item import ItemBase, SimpleItem


class PackageBase(ItemBase):
    r"""
    Base class for \usepackage and \RequirePackage
    """
    equal_attrs = ["name", "modifier_str"]
    __hash__ = EqHashMixin.__hash__

    def __init__(
            self, name: str, modifier_str: Optional[str] = None, eq_on_modifier: bool = True,
    ):
        r"""
        :param name: Name of LaTeX package
        :param modifier_str: any options to be passed to the LaTeX package. E.g. if 'abc=true'
            is passed, it will render as \usepackage[abc=true]{mypackage}
        :param eq_on_modifier: Whether to consider any package options when checking equality
            of the package. Useful to set it to False when this package should not be added
            if it was previously added with different options
        """
        self.name = name
        self.modifier_str = modifier_str
        self.eq_on_modifier = eq_on_modifier

    def __repr__(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def __eq__(self, other):
        try:
            eq_on_modifier = self.eq_on_modifier and other.eq_on_modifier
        except AttributeError:
            return False
        if not eq_on_modifier:
            try:
                return self.name == other.name
            except AttributeError:
                return False

        # Compare using modifier
        try:
            return all(
                [self.name == other.name, self.modifier_str == other.modifier_str]
            )
        except AttributeError:
            return False

    def matches_name(self, other):
        return self.name == other


class Package(PackageBase):
    r"""
    Represents LaTeX \usepackage{}, pass to Document if any custom LaTeX packages are needed.
    """

    def __repr__(self):
        return f"<Package(name={self.name})>"

    def __str__(self):
        return _usepackage_str(self.name, self.modifier_str)


class RequirePackage(PackageBase):
    r"""
    Represents LaTeX \RequirePackage, usually useful when building cls files and packages.
    """

    def __repr__(self):
        return f"<RequirePackage(name={self.name})>"

    def __str__(self):
        return _requirepackage_str(self.name, self.modifier_str)