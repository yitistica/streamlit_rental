import os
from pathlib import Path


def check_if_dir_exists(directory):
    return Path(directory).is_dir()


def set_working_directory(directory):
    os.chdir(directory)


def init_work_space(directory):
    pass