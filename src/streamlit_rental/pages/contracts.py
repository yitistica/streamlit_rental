import datetime

import streamlit as st
from streamlit_rental.rental.contracts import ContractTemplateConnection, RegularitiesConnection, TermsConnection
from streamlit_ace import st_ace


ace_setting = {'placeholder': "请拟定合同内容",
               'language': "markdown",
               'theme': 'github',
               'keybinding': 'sublime',
               'tab_size': 4,
               }


_default_title = ''
_default_content = ''

_saved_title = [_default_title]
_saved_content = [_default_content]


def add_template_section():
    my_expander = st.beta_expander("合同模板编辑", expanded=False)
    with my_expander:
        c1, c2 = st.beta_columns((1, 9))

        with c1:
            all_templates = ContractTemplateConnection().all_templates()
            all_templates.insert(0, (-1, '新模板'))
            selected_template = st.selectbox(label='选择合同模板',
                                             options=all_templates, key=f"模板选择",
                                             format_func=lambda x: x[1])

            font_size = st.slider("字体大小", 10, 52, 18)
            ace_setting['font_size'] = font_size
            render_button = st.button('排版', key=f"模板排版提交")
            save_button = st.button('存档', key=f"模板存档提交")
            clear_button = st.button('清空', key=f"模板清空提交")
            submit_button = st.button('模板入库', key=f"模板入库提交")

        with c2:
            if selected_template[0] == -1:  # new template
                _saved_title[0] = _default_title
                _saved_content[0] = _default_content
                title = st.text_input(label='模板标题', value=_saved_title[0], key='模板标题')
                content = st_ace(_saved_content[0], **ace_setting)
            else:
                template = ContractTemplateConnection().query_by_template_id(id_=selected_template[0])
                _saved_title[0] = template.template_title
                _saved_content[0] = template.template_content
                title = st.text_input(label='模板标题', value=_saved_title[0], key='模板标题')
                content = st_ace(_saved_content[0], **ace_setting)

            if save_button:
                _saved_title[0] = title
                _saved_content[0] = content

            if clear_button:
                _saved_content[0] = _default_content

            if submit_button:
                template_dict = {'create_time': datetime.datetime.now(),
                                 'update_time': datetime.datetime.now(),
                                 'create_author': 1,
                                 'update_author': 1,
                                 'template_title': title,
                                 'template_content': content}

                connection = ContractTemplateConnection()
                connection.add_by_dict(template_dict)
                connection.close()

                _saved_title[0] = _default_title
                _saved_content[0] = _default_content
                st.success(f'成功提交')

        with c2:
            st.markdown('#### 预览排版结果')
            if render_button:
                st.markdown(f"## {title}")
                st.markdown(content)
            else:
                st.markdown('')


def main():

    # add contract templates
    add_template_section()




