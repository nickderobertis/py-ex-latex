from pyexlatex.models.control.documentclass.classtypes.builtin_classes import BUILTIN_CLASS_TYPES
from pyexlatex.models.control.documentclass.classtypes.custom import CUSTOM_CLASS_TYPES
from pyexlatex.models.control.documentclass.classtypes.documentclasstype import DocumentClassType


class DocumentClassTypesManager:

    def __init__(self):
        pass

    def get_class_type_by_name(self, name: str) -> DocumentClassType:
        if self.is_builtin_class_type(name):
            return BUILTIN_CLASS_TYPES[name]

        if self.is_custom_class_type(name):
            return CUSTOM_CLASS_TYPES[name]

        raise NoSuchDocumentClassTypeException

    def is_custom_class_type(self, name: str) -> bool:
        return name in CUSTOM_CLASS_TYPES

    def is_builtin_class_type(self, name: str) -> bool:
        return name in BUILTIN_CLASS_TYPES


class NoSuchDocumentClassTypeException(Exception):
    pass
