import os
import shutil


def _move_if_needed(src, dst):
    try:
        shutil.move(src, dst)
    except shutil.SameFileError:
        pass


def _move_if_exists_and_is_needed(src, dst):
    if not os.path.exists(src):
        return

    _move_if_needed(src, dst)


def _move_folder_or_move_files_if_destination_folder_exists(src, dst):
    try:
        _move_if_needed(src, dst)
    except shutil.Error:
        files = [file for file in next(os.walk(src))[2]]
        [_move_if_needed(file, dst) for file in files]


def _copy_if_needed(src, dst):
    try:
        shutil.copy(src, dst)
    except shutil.SameFileError:
        pass