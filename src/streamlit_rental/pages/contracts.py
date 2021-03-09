import datetime

import streamlit as st
from streamlit_rental.rental.contract_builder import ContractTemplateConnection, RegularitiesConnection, TermsConnection
from streamlit_rental.rental.regularities import RegularityParser
from streamlit_ace import st_ace
from streamlit_rental.configs import STATE_DICT


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
    my_expander = st.beta_expander("增加合同模板", expanded=False)
    with my_expander:
        c1, c2, c3 = st.beta_columns((1, 1, 8))

        with c1:
            all_templates = ContractTemplateConnection().all_titles()
            all_template_titles = [template[1] for template in all_templates]
            all_templates.insert(0, (-1, '新模板'))
            selected_template = st.selectbox(label='选择合同模板',
                                             options=all_templates, key=f"模板选择",
                                             format_func=lambda x: x[1])

            font_size = st.slider("字体大小", 10, 52, 18)
            ace_setting['font_size'] = font_size
            render_button = st.button('排版', key=f"模板排版提交")
            save_button = st.button('存档', key=f"模板存档提交")
            clear_button = st.button('清空', key=f"模板清空提交")
            submit_button = st.button('新加模板入库', key=f"新加模板入库提交")

        with c3:
            if selected_template[0] == -1:  # new template
                _saved_title[0] = _default_title
                _saved_content[0] = _default_content
                title = st.text_input(label='模板标题', value=_saved_title[0], key='模板标题')
                content = st_ace(_saved_content[0], **ace_setting)
            else:
                template = ContractTemplateConnection().query_by_id(id_=selected_template[0])
                _saved_title[0] = template.title
                _saved_content[0] = template.content
                title = st.text_input(label='模板标题', value=_saved_title[0], key='模板标题')
                content = st_ace(_saved_content[0], **ace_setting)

            if save_button:
                _saved_title[0] = title
                _saved_content[0] = content

            if clear_button:
                _saved_content[0] = _default_content

        if submit_button:
            if title in all_template_titles:
                c1.error(f"命名<{title}>被占用，请使用另外一个命名。")
            elif len(title) < 5:
                c1.error(f"命名<{title}>太短，请使用另外一个命名。")
            else:
                template_dict = {'create_time': datetime.datetime.now(),
                                 'title': title,
                                 'content': content}

                connection = ContractTemplateConnection()
                connection.add_by_dict(template_dict)
                connection.close()

                _saved_title[0] = _default_title
                _saved_content[0] = _default_content
                c1.success(f'成功提交')

        with c3:
            st.markdown('#### 预览排版结果')
            if render_button:
                st.markdown(f"## {title}")
                st.markdown(content)
            else:
                st.markdown('')


def add_regularity_section():
    my_expander = st.beta_expander("增加常规项", expanded=False)
    with my_expander:
        c1, c2, c3, c4 = st.beta_columns((2, 1, 3, 1))

        with c1:
            all_regularities_sets = RegularitiesConnection().all_titles()
            all_regularities_set_titles = [regularities_set[1] for regularities_set in all_regularities_sets]
            all_regularities_sets.insert(0, (-1, '新常规项集'))
            selected_regularities_set = st.selectbox(label='选择常规项设定',
                                                     options=all_regularities_sets, key=f"常规项选择",
                                                     format_func=lambda x: x[1])

            title = st.text_input(label='常规项集标题', value='', key='新常规项集标题')
            submit_button = st.button('新加常规项集入库', key=f"新加常规项集入库提交")

        with c3:
            new_regularities = list()
            if selected_regularities_set[0] == -1:  # new regularity set:
                regularities = RegularityParser().all()
            else:
                regularities_set = RegularitiesConnection().query_by_id(id_=selected_regularities_set[0])
                regularities = RegularitiesConnection.convert_set_str_to_dicts(regularities_set.set)

            for regularity in regularities:
                default_price = regularity['price']
                incremental_step = max(int(default_price / 5), 1)
                set_price = st.number_input(
                    label=f"{regularity['item']} {regularity['frequency']}",
                    value=default_price,
                    step=incremental_step,
                    key=f"{regularity['type']}_{regularity['item']}_input")

                new_regularity = regularity.copy()
                new_regularity['price'] = set_price
                new_regularities.append(new_regularity)

        if submit_button:
            if title in all_regularities_set_titles:
                c1.error(f"命名<{title}>被占用，请使用另外一个命名。")
            elif len(title) < 5:
                c1.error(f"命名<{title}>太短，请使用另外一个命名。")
            else:
                regularities_set_dict = {'create_time': datetime.datetime.now(),
                                         'title': title,
                                         'set': RegularitiesConnection.convert_dicts_to_set_str(new_regularities)}

                connection = RegularitiesConnection()
                connection.add_by_dict(regularities_set_dict)
                connection.close()
                c1.success(f'成功提交')


def assemble_term_structure():
    my_expander = st.beta_expander("增加最终条款", expanded=False)
    with my_expander:
        c1, c2, c3, c4 = st.beta_columns((2, 1, 4, 1))

        with c1:
            # terms:
            all_terms = TermsConnection().all_titles()
            all_terms_titles = [term[1] for term in all_terms]
            all_terms.insert(0, (-1, '新条款集'))

            # templates:
            all_templates = ContractTemplateConnection().all_titles()
            selected_template = st.selectbox(label='选择合同模板',
                                             options=all_templates, key=f"模板选择 view_only",
                                             format_func=lambda x: x[1])

            # regularties:
            all_regularities_sets = RegularitiesConnection().all_titles()
            selected_regularities_set = st.selectbox(label='选择常规项集',
                                                     options=all_regularities_sets, key=f"常规项选择 view_only",
                                                     format_func=lambda x: x[1])

            title = st.text_input(label='条款集标题', key='新条款集标题')

            submit_button = st.button('增加条款集', key=f"增加条款集入库提交")

        with c3:
            if selected_template:
                template = ContractTemplateConnection().query_by_id(id_=selected_template[0])
                st.markdown(template.content)

            if selected_regularities_set:
                regularities_set = RegularitiesConnection().query_by_id(id_=selected_regularities_set[0])
                regularities_set_df = RegularitiesConnection.convert_dicts_to_df(regularities_set.set)
                regularities_set_df = regularities_set_df[regularities_set_df['价格'] > 0].reset_index(drop=True)
                st.table(regularities_set_df)

        if submit_button:
            if title in all_terms_titles:
                c1.error(f"命名<{title}>被占用，请使用另外一个命名。")
            elif len(title) < 5:
                c1.error(f"命名<{title}>太短，请使用另外一个命名。")
            else:
                term_dict = {
                    'title': title,
                    'create_time': datetime.datetime.now(),
                    'template': template.id,
                    'regularities': regularities_set.id}

                connection = TermsConnection()
                connection.add_by_dict(term_dict)
                connection.close()
                c1.success(f'成功提交')


def main():

    # add contract templates
    add_template_section()

    # regularity section:
    add_regularity_section()

    # assemble terms:
    assemble_term_structure()

