from typing import Optional, Callable, Tuple
import warnings
from pyexlatex.logic.output.errors.exc import TooManyUnprocessedFloatsException
from pyexlatex.models.control.extrafloats import ExtraFloats

EXTRA_FLOATS_LIMIT = 10000
DEFAULT_EXTRA_FLOATS = 1000
FLOATS_INCREASE_FACTOR = 2

def get_extra_float_and_new_num_floats(extra_floats_num: Optional[int] = None) -> Tuple[ExtraFloats, int]:
    if extra_floats_num is None:
        num_floats = DEFAULT_EXTRA_FLOATS
    else:
        num_floats = extra_floats_num * FLOATS_INCREASE_FACTOR
    if num_floats > EXTRA_FLOATS_LIMIT:
        raise TooManyUnprocessedFloatsException(f'tried increasing max floats, '
                                                f'but hit limit of {EXTRA_FLOATS_LIMIT} floats')
    extra_float = ExtraFloats(num_floats)
    return extra_float, num_floats

# def handle_too_many_floats_exception(latex_str: str, callback: Callable, extra_floats_num: Optional[int] = None,
#                                      **callback_kwargs):
#     from pyexlatex.logic.builder import _build
#
#     if extra_floats_num is None:
#         num_floats = DEFAULT_EXTRA_FLOATS
#     else:
#         num_floats = extra_floats_num * FLOATS_INCREASE_FACTOR
#     if num_floats > EXTRA_FLOATS_LIMIT:
#         raise TooManyUnprocessedFloatsException(f'tried increasing max floats, '
#                                                 f'but hit limit of {EXTRA_FLOATS_LIMIT} floats')
#     extra_float = ExtraFloats(num_floats)
#     modified_str = _build([extra_float, latex_str])
#     warnings.warn(f'could not create pdf due to too many unprocessed floats. trying again '
#                   f'with {num_floats} extra floats')
#     return callback(modified_str, extra_floats_num=num_floats, **callback_kwargs)
