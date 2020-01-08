from typing import Union, List, Tuple, Dict, Optional

from pyexlatex.models.item import Item, ItemBase
from pyexlatex.models.documentitem import DocumentItem

AnyItem = ItemBase
ListOfItems = List[ItemBase]
DictOfItems = Dict[str, AnyItem]
ListOrDictOfItems = Union[ListOfItems, DictOfItems]
ListOrDictOrItem = Union[ListOrDictOfItems, AnyItem]
ItemOrListOfItems = Union[AnyItem, ListOfItems]
StrList = List[str]
StrListOrNone = Union[StrList, None]
BytesList = List[bytes]
BytesListOrNone = Optional[BytesList]
ItemAndPreEnvContents = Tuple[AnyItem, StrListOrNone]