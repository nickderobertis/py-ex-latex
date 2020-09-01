from typing import List, Optional, Sequence, Union

from pyexlatex.exc import NoPackageWithNameException
from pyexlatex.models.documentitem import DocumentItem
from pyexlatex.models.package import Package
from mixins.repr import ReprMixin
from mixins.attrequals import EqOnAttrsMixin, EqHashMixin
from pyexlatex.models.references.bibtex.base import BibTexEntryBase


class UniqueDataList(list):
    """
    A list where the items are always unique.
    """

    def __init__(self, iterable):
        if iterable is None:
            iterable = []
        super().__init__(iterable)

    def append(self, value):
        if value is None:
            return
        if value in self:
            return
        return super().append(value)

    def extend(self, iterable):
        if iterable is None:
            return
        new_items = [item for item in iterable if item not in self]
        if not new_items:
            return
        return super().extend(new_items)


class UniquePackagesList(UniqueDataList):
    """
    A unique data list that allows passing of just a string to represent a package
    """

    def __init__(self, packages: Optional[List[Union[Package, str]]] = None):
        if packages is None:
            packages = []

        packages = self._as_packages(packages)

        super().__init__(packages)

    def _as_package(self, package: Union[Package, str]):
        if isinstance(package, str):
            return Package(package)

        return package

    def _as_packages(self, packages: Optional[List[Union[Package, str]]] = None):
        if packages is None:
            return packages
        return [self._as_package(pack) for pack in packages]

    def append(self, package: Union[Package, str]):
        if package is None:
            return
        package = self._as_package(package)
        super().append(package)

    def extend(self, packages: Optional[List[Union[Package, str]]] = None):  # type: ignore
        if packages is None:
            return
        packages = self._as_packages(packages)
        super().extend(packages)

    def get_by_name(self, name: str):
        for package in self:
            if package.matches_name(name):
                return package
        raise NoPackageWithNameException(name)

    def delete_by_name(self, name: str):
        new_packages = []
        for package in self:
            if not hasattr(package, 'matches_name'):
                # Got something other than a package
                # TODO [#13]: think about how to delete non-packages from packages
                new_packages.append(package)  # No way to check if name matches, so just keep it
            elif not package.matches_name(name):
                new_packages.append(package)
        if len(new_packages) == len(self):
            raise NoPackageWithNameException(name)

        super().__init__(new_packages)


class DocumentSetupData(ReprMixin, EqOnAttrsMixin, EqHashMixin):
    repr_cols = [
        'filepaths',
        'begin_document_items',
        'end_document_items',
        'packages',
        'source_paths',
        'references',
        'flags'
    ]
    ignore_attrs = [
        'ignore_attrs',
        'repr_cols',
        'attrs',
        'readable_repr',
        'equal_attrs'
    ]
    equal_attrs = [
        'filepaths',
        'binaries',
        'begin_document_items',
        'end_document_items',
        'packages',
        'source_paths',
        'references',
        'flags'
    ]
    non_unique_attrs = [
        'filepaths',
        'binaries'
    ]

    def __init__(self, filepaths: Optional[List[str]] = None, binaries: Optional[List[bytes]] = None, 
                 begin_document_items: Optional[List[DocumentItem]] = None, 
                 end_document_items: Optional[List[DocumentItem]] = None, packages: Optional[List[Union[Package, str]]] = None,
                 source_paths: Optional[List[str]] = None, references: Optional[Sequence[BibTexEntryBase]] = None,
                 flags: Optional[List[str]] = None):
        self.filepaths = UniqueDataList(filepaths)
        self.binaries = UniqueDataList(binaries)
        self.begin_document_items = UniqueDataList(begin_document_items)
        self.end_document_items = UniqueDataList(end_document_items)
        self.packages = UniquePackagesList(packages)
        self.source_paths = UniqueDataList(source_paths)
        self.references = UniqueDataList(references)
        self.flags = UniqueDataList(flags)

    @property
    def attrs(self) -> List[str]:
        return [attr for attr in dir(self) if (not attr.startswith('_') and not attr in self.ignore_attrs)]