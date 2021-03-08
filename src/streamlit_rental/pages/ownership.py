import streamlit as st
from streamlit_rental.rental.owner import OwnerConnection
from streamlit_rental.pages.utils.section_grid import add_simple_form


def add_owner_section():
    my_expander = st.beta_expander("增加所有者", expanded=False)
    with my_expander:
        connection = OwnerConnection()
        c1, c2, c3 = st.beta_columns((1, 4, 1))
        add_simple_form(column=c2, connection=connection, key='add_owner', ignore=['id'])


def main():
    # add owner
    add_owner_section()




