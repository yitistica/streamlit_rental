import streamlit as st
from streamlit_rental.utils.sys import check_if_dir_exists, get_working_directory, \
    set_working_directory, get_child_directories
from streamlit_rental.rental.init_application import create_app


def _status_indication():
    pass


def _set_workspace(directory):
    if check_if_dir_exists(directory=directory):
        set_working_directory(directory=directory)
        st.success('完成设置工作空间。')
    else:
        st.error(f'路径<{directory}>不存在，请重新设置。')


def set_workspace():
    c1, c2, c3 = st.beta_columns((1, 5, 1))
    set_dir = c2.text_input("工作空间路径，e.g., C:/Users/workspace/",
                            'C:/Users/yeech/Desktop/streamlit_rental_working_directory')
    set_button = c2.button("更改", key='change working dir buttom')
    if set_dir and set_button:
        _set_workspace(directory=set_dir)


def _set_app(directory, app_name):
    pass


def set_app():
    c1, c2, c3 = st.beta_columns((1, 5, 1))
    working_directory_path = get_working_directory()
    app_dirs, folder_names = get_child_directories(working_directory_path)
    selected_app = c2.selectbox("APP 地址", folder_names)
    set_button = c2.button("选择 APP", key='set app button')

    if selected_app and set_button:
        # check all the file names:
        _set_app(directory=working_directory_path, app_name=selected_app)
        st.success('完成设置APP。')


def _init_new_app(directory):
    if check_if_dir_exists(directory=directory):
        create_app(dir_path=directory)
        st.success('完成创建新的管理APP。')
        _set_workspace(directory)
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

    my_expander = st.beta_expander("选择 APP", expanded=False)
    with my_expander:
        set_app()

    my_expander = st.beta_expander("创建新的管理 APP", expanded=False)
    with my_expander:
        init_new_app()




