from typing import List, Optional
from dero.latex.models.documentitem import DocumentItem
from dero.latex.models.package import Package
from dero.mixins.repr import ReprMixin
from dero.mixins.attrequals import EqOnAttrsMixin, EqHashMixin


class UniqueDataList(list):

    def __init__(self, iterable):
        if iterable is None:
            iterable = []
        return super().__init__(iterable)

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


class DocumentSetupData(ReprMixin, EqOnAttrsMixin, EqHashMixin):
    repr_cols = [
        'filepaths',
        'begin_document_items',
        'end_document_items',
        'packages',
        'source_paths'
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
        'source_paths'
    ]

    def __init__(self, filepaths: Optional[List[str]] = None, binaries: Optional[List[bytes]] = None, 
                 begin_document_items: Optional[List[DocumentItem]] = None, 
                 end_document_items: Optional[List[DocumentItem]] = None, packages: Optional[List[Package]] = None,
                 source_paths: Optional[List[str]] = None):
        self.filepaths = UniqueDataList(filepaths)
        self.binaries = UniqueDataList(binaries)
        self.begin_document_items = UniqueDataList(begin_document_items)
        self.end_document_items = UniqueDataList(end_document_items)
        self.packages = UniqueDataList(packages)
        self.source_paths = UniqueDataList(source_paths)

    @property
    def attrs(self) -> List[str]:
        return [attr for attr in dir(self) if (not attr.startswith('_') and not attr in self.ignore_attrs)]