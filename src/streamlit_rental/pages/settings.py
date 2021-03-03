import streamlit as st
from streamlit_rental.utils.sys import check_if_dir_exists, set_working_directory


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


def main():
    my_expander = st.beta_expander("根工作空间设置", expanded=False)
    with my_expander:
        set_workspace()





