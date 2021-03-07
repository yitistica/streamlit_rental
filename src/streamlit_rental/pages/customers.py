import streamlit as st
from streamlit_rental.rental.manager import ManagerConnection, OwnerConnection
from streamlit_rental.pages.utils.section_grid import add_simple_form


def _individual_manager_card():
    pass


def add_customer_section():
    my_expander = st.beta_expander("增加住户", expanded=False)
    with my_expander:
        manager_connection = ManagerConnection()
        c1, c2, c3 = st.beta_columns((1, 4, 1))
        add_simple_form(column=c2, connection=manager_connection, key='add_manager', ignore=['id'])


def main():

    # add customer
    add_customer_section()




