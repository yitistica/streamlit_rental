import streamlit as st
from streamlit_rental.configs import STATE_DICT


def main():
    my_expander = st.beta_expander("查看", expanded=True)
    with my_expander:
        st.markdown(STATE_DICT)





