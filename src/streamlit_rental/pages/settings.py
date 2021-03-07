import streamlit as st
from streamlit_rental.utils.sys import check_if_dir_exists, get_working_directory, \
    set_working_directory, get_child_directories, join_paths
from streamlit_rental.rental.init_application import create_app
from streamlit_rental.rental.connections import Session_factory
from streamlit_rental.configs import STATE_DICT, DEFAULT_WORK_SPACE_PATH, DB_NAME
from streamlit_rental.utils.display_components import convert_a_dict_to_table


def _status_indication():
    info_dict = dict()
    # info_dict['APP 名字'] = STATE_DICT['configs']['app_name']
    # info_dict['APP 地址'] = STATE_DICT['configs']['app_path']
    # info_dict['数据库地址'] = STATE_DICT['configs']['app_db_path']
    info_dict['SQLAchemy Session'] = STATE_DICT['Session']

    info_df = convert_a_dict_to_table(info_dict)
    info_df.columns = ['信息']
    return info_df


def show_status_indication():
    c1, c2, c3 = st.beta_columns((1, 8, 1))
    status_df = _status_indication()
    c2.table(status_df)


def set_workspace_to_dir(directory):
    if check_if_dir_exists(directory=directory):
        set_working_directory(directory=directory)
        STATE_DICT['configs']['workspace_path'] = directory
        st.success('完成设置工作空间。')
    else:
        st.error(f'路径<{directory}>不存在，请重新设置。')


def set_workspace():
    c1, c2, c3 = st.beta_columns((1, 5, 1))
    set_dir = c2.text_input("工作空间路径，e.g., C:/Users/workspace/", DEFAULT_WORK_SPACE_PATH)
    set_button = c2.button("更改", key='change working dir buttom')
    if set_dir and set_button:
        set_workspace_to_dir(directory=set_dir)


def set_app_dir(directory, app_name):
    STATE_DICT['configs']['app_name'] = app_name
    STATE_DICT['configs']['app_path'] = join_paths(directory, app_name)
    STATE_DICT['configs']['app_db_path'] = join_paths(STATE_DICT['configs']['app_path'], DB_NAME)

    Session_factory()  # set section to STATE_DICT


def set_app():
    c1, c2, c3 = st.beta_columns((1, 5, 1))
    working_directory_path = get_working_directory()
    app_dirs, folder_names = get_child_directories(working_directory_path)
    selected_app = c2.selectbox("APP 地址", folder_names)
    set_button = c2.button("选择 APP", key='set app button')

    if selected_app and set_button:
        # check all the file names:
        set_app_dir(directory=working_directory_path, app_name=selected_app)
        st.success('完成设置APP。')


def _init_new_app(directory):
    if check_if_dir_exists(directory=directory):
        create_app(dir_path=directory)
        st.success('完成创建新的管理APP。')
        set_workspace_to_dir(directory)
    else:
        st.error(f'路径<{directory}>不存在，请重新设置。')


def init_new_app():
    c1, c2, c3 = st.beta_columns((1, 5, 1))
    working_directory_path = get_working_directory()
    set_dir = c2.text_input("设置工作路径，e.g., C:/Users/workspace/", working_directory_path)

    set_button = c2.button("创建 APP", key='create app button')
    if set_dir and set_button:
        # check all the file names:
        _init_new_app(directory=set_dir)


def main():
    my_expander = st.beta_expander("根工作空间设置", expanded=False)
    with my_expander:
        set_workspace()

    my_expander = st.beta_expander("选择管理 APP", expanded=False)
    with my_expander:
        set_app()

    my_expander = st.beta_expander("创建新的管理 APP", expanded=False)
    with my_expander:
        init_new_app()
