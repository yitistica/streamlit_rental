import streamlit as st
from streamlit_rental.pages import settings

import os

PAGES = {
    "设置": settings,
}


def main():
    title = st.empty()
    st.sidebar.title("房屋管理平台")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]
    page.main()


