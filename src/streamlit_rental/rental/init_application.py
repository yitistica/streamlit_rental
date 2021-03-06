"""
workspace:
    app:


"""
import datetime

from streamlit_rental.configs import DEFAULT_APP_FOLDER_PREFIX, DB_NAME
from streamlit_rental.data_models import create_sqlite_engine, create_tables
from streamlit_rental.utils.sys import join_paths, create_folder


def _create_app_folder_name():
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    folder_name = F"{DEFAULT_APP_FOLDER_PREFIX}_{now_str}"
    return folder_name


def init_database(dir_path, db_name):
    db_path = join_paths(dir_path=dir_path, sub_dir_path=db_name)
    engine = create_sqlite_engine(db_path, echo=True)
    create_tables(engine=engine)


def create_app(dir_path):
    # create app folder:
    app_folder_name = _create_app_folder_name()
    app_path = create_folder(dir_path=dir_path, folder_name=app_folder_name)

    # create db:
    init_database(dir_path=app_path, db_name=DB_NAME)
