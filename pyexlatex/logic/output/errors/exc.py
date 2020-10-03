"""
Add exceptions here and set _match_str to whatever string should match the exception. They will automatically
be passed to the exception manager
"""
import sys
import inspect
from pyexlatex.logic.output.errors.models.exception_manager import LatexExceptionManager


class LatexException(Exception):
    _match_str = ''


class TooManyUnprocessedFloatsException(LatexException):
    _match_str = 'Too many unprocessed floats'


class OutputLoopConsecutiveDeadCycles(LatexException):
    _match_str = 'consecutive dead cycles'

####### Exception Manager Logic (only define specific exceptions above here) #############

exception_classes =  [class_tuple[1] for class_tuple in inspect.getmembers(sys.modules[__name__], inspect.isclass)]
excluded_classes = [
    LatexException,
    LatexExceptionManager
]
specific_exception_classes = [klass for klass in exception_classes if klass not in excluded_classes]
exception_manager = LatexExceptionManager(specific_exception_classes)