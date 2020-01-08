import shutil
import os
import time
from typing import Iterable, Callable, Optional


def move_if_exists(inpath: str, outpath: str, retries: int = 3, sleep_time: float = 0.1) -> None:
    _run_func_handling_file_modify_exceptions(
        shutil.move,
        inpath,
        outpath,
        func_short_desc='move',
        retries_remaining=retries,
        sleep_time=sleep_time
    )


def remove_all_if_exist(filepaths: Iterable[str]):
    [remove_if_exists(filepath) for filepath in filepaths]


def remove_if_exists(filepath: str, retries: int = 3, sleep_time: float = 0.1):
    _run_func_handling_file_modify_exceptions(
        os.remove,
        filepath,
        func_short_desc='delete',
        retries_remaining=retries,
        sleep_time=sleep_time
    )


def move_all_if_exists(inpaths: Iterable[str], outfolder: str) -> None:
    for inpath in inpaths:
        move_if_exists(inpath, outfolder)


def _run_func_handling_file_modify_exceptions(func: Callable, filepath: str, *args,
                                              func_short_desc: Optional[str] = None, retries_remaining: int = 3,
                                              sleep_time: float = 0.1,
                                              **kwargs) -> None:
    if retries_remaining < 0:
        raise PermissionError(f'could not modify {filepath}, even after retrying')

    func_desc = _get_func_short_description(func, func_short_desc)

    try:
        func(filepath, *args, **kwargs)
    except FileNotFoundError:
        print(f'Cannot {func_desc}: did not find {filepath}')
        return
    except PermissionError:
        # Retry with waits before determining that the file cannot be modified
        time.sleep(sleep_time)
        return _run_func_handling_file_modify_exceptions(
            func,
            filepath,
            *args,
            func_short_desc=func_short_desc,
            retries_remaining=retries_remaining - 1,
            sleep_time=sleep_time
        )



def _get_func_short_description(func: Callable, func_short_desc: Optional[str] = None) -> str:
    if func_short_desc is None:
        return f'call {func.__name__}'
    else:
        return func_short_desc