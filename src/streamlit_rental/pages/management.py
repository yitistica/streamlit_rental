import streamlit as st
from streamlit_rental.configs import STATE_DICT


def _individual_manager_card():
    pass



def _add_manager(**kwargs):
    pass



def main():
    my_expander = st.beta_expander("管理者", expanded=False)
    with my_expander:
        st.markdown(STATE_DICT)





