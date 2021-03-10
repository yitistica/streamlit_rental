import streamlit as st
from streamlit_rental.rental.property import OwnerConnection, PropertyConnection
from streamlit_rental.pages.utils.section_grid import add_simple_form


def add_owner_section():
    my_expander = st.beta_expander("增加所有者", expanded=False)
    with my_expander:
        c1, c2, c3 = st.beta_columns((1, 3, 1))
        add_simple_form(selection_column=c1, column=c2, Connection=OwnerConnection, key='add_owner', ignore=['id'])


def add_property_section():
    my_expander = st.beta_expander("增加产权", expanded=False)
    with my_expander:
        c1, c2, c3 = st.beta_columns((1, 3, 1))
        add_simple_form(selection_column=c1, column=c2, Connection=PropertyConnection, key='add_property', ignore=['id'])


def main():
    # add owner
    add_owner_section()

    # add property
    add_property_section()





