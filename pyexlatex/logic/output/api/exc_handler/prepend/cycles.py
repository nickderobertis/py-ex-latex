from typing import Optional, Callable, Tuple
import warnings
from pyexlatex.logic.output.errors.exc import OutputLoopConsecutiveDeadCycles
from pyexlatex.models.control.maxdeadcycles import MaxDeadCycles

EXTRA_CYCLES_LIMIT = 1000
DEFAULT_EXTRA_CYCLES = 200
CYCLES_INCREASE_FACTOR = 2


def get_max_dead_cycles_and_new_num_cycles(cycles_num: Optional[int] = None) -> Tuple[MaxDeadCycles, int]:
    if cycles_num is None:
        cycles = DEFAULT_EXTRA_CYCLES
    else:
        cycles = cycles_num * CYCLES_INCREASE_FACTOR
    if cycles > EXTRA_CYCLES_LIMIT:
        raise OutputLoopConsecutiveDeadCycles(f'tried increasing max consecutive dead cycles, '
                                                f'but hit limit of {EXTRA_CYCLES_LIMIT} cycles')
    max_cycles = MaxDeadCycles(cycles)
    return max_cycles, cycles


def handle_output_loop_cycles_exception(latex_str: str, callback: Callable, cycles_num: Optional[int] = None,
                                        **callback_kwargs):
    from pyexlatex.logic.builder import _build

    if cycles_num is None:
        cycles = DEFAULT_EXTRA_CYCLES
    else:
        cycles = cycles_num * CYCLES_INCREASE_FACTOR
    if cycles > EXTRA_CYCLES_LIMIT:
        raise OutputLoopConsecutiveDeadCycles(f'tried increasing max consecutive dead cycles, '
                                                f'but hit limit of {EXTRA_CYCLES_LIMIT} cycles')
    max_cycles = MaxDeadCycles(cycles)
    modified_str = _build([max_cycles, latex_str])
    warnings.warn(f'could not create pdf due to too many consecutive dead cycles. trying again with {cycles} cycles')
    return callback(modified_str, cycles_num=cycles, **callback_kwargs)
