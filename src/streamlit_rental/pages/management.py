import streamlit as st
from streamlit_rental.configs import STATE_DICT
from streamlit_rental.rental.manager import ManagerConnection


def _individual_manager_card():
    pass


def _add_manager(**kwargs):
    manager_connection = ManagerConnection()
    manager_connection.add_manager(**kwargs)
    manager_connection.close()


def main():
    my_expander = st.beta_expander("管理者", expanded=False)
    with my_expander:
        manager_connection = ManagerConnection()

        st.markdown(manager_connection.get_table_column_desc())





