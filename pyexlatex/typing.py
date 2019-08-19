from typing import Union, List, Tuple, Dict, Optional

from pyexlatex.models import Item
from pyexlatex.models.documentitem import DocumentItem

AnyItem = Union[Item, DocumentItem]
ListOfItems = List[AnyItem]
DictOfItems = Dict[str, AnyItem]
ListOrDictOfItems = Union[ListOfItems, DictOfItems]
ListOrDictOrItem = Union[ListOrDictOfItems, AnyItem]
ItemOrListOfItems = Union[AnyItem, ListOfItems]
StrList = List[str]
StrListOrNone = Union[StrList, None]
BytesList = List[bytes]
BytesListOrNone = Optional[BytesList]
ItemAndPreEnvContents = Tuple[AnyItem, StrListOrNone]