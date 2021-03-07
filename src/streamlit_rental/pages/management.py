import streamlit as st
from streamlit_rental.configs import STATE_DICT
from streamlit_rental.rental.manager import ManagerConnection
from streamlit_rental.pages.utils.section_grid import add_simple_form


def _individual_manager_card():
    pass


def add_manager_section():
    manager_connection = ManagerConnection()
    c1, c2, c3 = st.beta_columns((1, 4, 1))
    add_simple_form(column=c2, connection=manager_connection, key='add_manager', ignore=['id'])


def main():
    my_expander = st.beta_expander("增加管理者", expanded=False)
    with my_expander:
        add_manager_section()

        # st.markdown(manager_connection.get_table_column_desc())





