import streamlit as st
from streamlit_rental.pages import settings, contract_builder, properties, customers, admission
from streamlit_rental.configs import STATE_DICT, DEFAULT_WORK_SPACE_PATH

PAGES = {
        '新合同': admission,
        '客户管理': customers,
        '合同模板': contract_builder,
        '房屋管理': properties,
        "设置": settings,
    }


def _init_app():

    folder_names = []

    # init working dir:
    if 'workspace_path' not in STATE_DICT['configs']:
        settings.set_workspace_to_dir(directory=DEFAULT_WORK_SPACE_PATH)
        app_dirs, folder_names = settings.get_child_directories(DEFAULT_WORK_SPACE_PATH)
        folder_names.sort(reverse=True)

    # init app dir:
    if ('workspace_path' in STATE_DICT['configs']) and ('app_path' not in STATE_DICT['configs']) and folder_names:
        app_folder_name = folder_names[0]
        settings.set_app_dir(directory=DEFAULT_WORK_SPACE_PATH, app_name=app_folder_name)
    elif 'app_path' in STATE_DICT['configs']:
        pass
    else:
        st.warning('无可用管理 APP，请建立管理 APP。')


def main():
    _init_app()

    title = st.empty()
    st.sidebar.title("房屋管理平台")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]
    page.main()

