from typing import Optional, Dict, Any, List, Tuple
from pyexlatex.logic.output.errors.exc import (
    TooManyUnprocessedFloatsException,
    OutputLoopConsecutiveDeadCycles,
    LatexException
)
from pyexlatex.logic.output.api.exc_handler.prepend.floats import get_extra_float_and_new_num_floats
from pyexlatex.logic.output.api.exc_handler.prepend.cycles import get_max_dead_cycles_and_new_num_cycles
from pyexlatex.logic.output.api.exc_handler.prepend.typing import PrependItemsDict, PrependKwargsDict


def handle_prepend_exceptions(exceptions: List[LatexException], prepend_kwarg_dict: PrependKwargsDict = None,
                              prepend_items_dict: PrependItemsDict = None
                              ) -> Tuple[PrependItemsDict, PrependKwargsDict, List[LatexException]]:
    if prepend_items_dict is None:
        prepend_items_dict = {}
    unhandled_exceptions = []
    for exception in exceptions:
        try:
            prepend_item, prepend_kwarg_dict = get_data_to_handle_prepend_exception(exception, prepend_kwarg_dict)
            # Assigning to class as key ensures that there will only be one item of each type
            prepend_items_dict[type(prepend_item)] = prepend_item
        except LatexException as e:
            unhandled_exceptions.append(e)
    return prepend_items_dict, prepend_kwarg_dict, unhandled_exceptions


def get_data_to_handle_prepend_exception(exception: LatexException, prepend_kwarg_dict: PrependKwargsDict = None
                                         ) -> Tuple[Any, PrependKwargsDict]:

    prepend_kwarg_dict = get_prepend_kwarg_dict(prepend_kwarg_dict)

    try:
        raise exception
    except TooManyUnprocessedFloatsException:
        extra_float, new_num_floats = get_extra_float_and_new_num_floats(prepend_kwarg_dict['extra_floats_num'])
        prepend_kwarg_dict['extra_floats_num'] = new_num_floats
        return extra_float, prepend_kwarg_dict
    except OutputLoopConsecutiveDeadCycles:
        max_dead_cycles, new_num_cycles = get_max_dead_cycles_and_new_num_cycles(prepend_kwarg_dict['cycles_num'])
        prepend_kwarg_dict['cycles_num'] = new_num_cycles
        return max_dead_cycles, prepend_kwarg_dict


def get_prepend_kwarg_dict(prepend_kwarg_dict: PrependKwargsDict = None) -> Dict[str, Any]:
    if prepend_kwarg_dict is None:
        prepend_kwarg_dict = {}

    required_keys = [
        'extra_floats_num',
        'cycles_num'
    ]

    for key in required_keys:
        if key not in prepend_kwarg_dict:
            prepend_kwarg_dict[key] = None

    return prepend_kwarg_dict


def add_prepend_items_dict_to_latex_str(prepend_items_dict: PrependItemsDict, latex_str: str) -> str:
    from pyexlatex.logic.builder import _build
    if not prepend_items_dict:
        return latex_str
    prepend_items = [str(item) for item in prepend_items_dict.values()]
    return _build(prepend_items + [latex_str])