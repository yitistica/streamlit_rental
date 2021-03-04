import streamlit as st


def main():
    my_expander = st.beta_expander("查看", expanded=True)
    with my_expander:
        set_workspace()





