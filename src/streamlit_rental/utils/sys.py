import os
from pathlib import Path


def check_if_dir_exists(directory):
    return Path(directory).is_dir()


def get_working_directory():
    return os.getcwd()


def get_child_directories(directory):
    child_dirs = []
    folder_names = []
    for path in Path(directory).iterdir():
        if path.is_dir():
            child_dirs.append(path)
            folder_names.append(path.name)
    return child_dirs, folder_names


def set_working_directory(directory):
    os.chdir(directory)


def join_paths(dir_path, sub_dir_path):
    path = Path(dir_path).joinpath(sub_dir_path)
    return path


def create_folder(dir_path, folder_name):
    path = Path(dir_path).joinpath(folder_name)
    path.mkdir(parents=False, exist_ok=False)
    return path
