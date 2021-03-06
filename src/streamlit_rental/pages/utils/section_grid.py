import datetime
import streamlit as st

global_value_translations = {}


global_column_translations = {}


def add_simple_form(selection_st_column, main_st_column, Connection, key, ignore):
    with selection_st_column:
        connection = Connection()
        all_instances = connection.all()  # with all method
        new_instance = connection.instanate_orm()
        all_instances.insert(0, new_instance)

        label = connection.get_table_alias()
        selected_instance = st.selectbox(label=f'选择{label}',
                                         options=all_instances, key=f"选择{label}",
                                         format_func=lambda x: Connection.make_label(x))

        submit_button = st.button('提交', key=f"{key}_{label}_submit")
        cancel_button = st.button('取消', key=f"{key}_{label}_cancel")

    with main_st_column:
        col_desc = connection.get_table_column_desc()
        table_name = connection.get_table_name()
        form = dict()
        for col, column_info in col_desc.items():
            # key:
            col_key = f"{key}_{col}"

            # label:
            if (table_name in global_column_translations) and (col in global_column_translations[table_name]):
                col_label = global_column_translations[table_name][col]
            elif column_info['comment']:
                col_label = column_info['comment']
            else:
                col_label = col

            # default:
            if not selected_instance.id:
                default = column_info['default']
            else:
                default = getattr(selected_instance, col)

            if col in ignore:
                continue
            else:
                if column_info['type'] == 'date':
                    if not default:
                        default = datetime.datetime.now().date()
                    col_input = main_st_column.date_input(label=col_label,
                                                          value=default,
                                                          key=col_key)
                elif column_info['type'] == 'datetime':
                    if not default:
                        default = datetime.datetime.now()
                    col_input = main_st_column.date_input(label=col_label,
                                                          value=default,
                                                          key=col_key)
                elif column_info['type'] == 'bool':
                    if not default:
                        default = False
                    col_input = main_st_column.checkbox(label=col_label,
                                                        value=default,
                                                        key=col_key)
                elif column_info['type'] in ['int', 'float']:
                    if not default:
                        col_input = main_st_column.number_input(label=col_label,
                                                                key=col_key)
                    else:
                        col_input = main_st_column.number_input(label=col_label,
                                                                value=default,
                                                                key=col_key)

                    if column_info['type'] == 'int':
                        col_input = int(col_input)
                    else:
                        col_input = float(col_input)
                elif column_info['type'] == 'choice':
                    choices = column_info['choices']
                    col_input = main_st_column.selectbox(label=col_label,
                                                         options=choices,
                                                         index=0,
                                                         key=col_key)
                else:  # str
                    if not default:
                        col_input = main_st_column.text_input(label=col_label,
                                                              key=col_key)
                    else:
                        col_input = main_st_column.text_input(label=col_label,
                                                              value=default,
                                                              key=col_key)

            form[col] = col_input

        if submit_button:
            for col, col_input in form.items():
                if (not col_desc[col]['nullable']) and (not form[col]):
                    main_st_column.error(f'字段<{col}>不能为空。')
                    main_st_column.stop()

            if not selected_instance.id:  # new
                connection.add_by_dict(form)
                connection.close()
            else:
                selected_instance = connection.query_by_id(id_=selected_instance.id)
                for col, value in form.items():
                    setattr(selected_instance, col, value)
                connection.commit()
                connection.close()

            main_st_column.success(f'成功提交')

        elif cancel_button:
            st.stop()


def add_form_with_foreign_keys(selection_st_column, main_st_column, Connection, foreign_Connections, key, ignore):
    with selection_st_column:
        connection = Connection()
        all_instances = connection.all()  # with all method
        new_instance = connection.instanate_orm()
        all_instances.insert(0, new_instance)

        label = connection.get_table_alias()
        selected_instance = st.selectbox(label=f'选择{label}',
                                         options=all_instances, key=f"选择{label}",
                                         format_func=lambda x: Connection.make_label(x))

        submit_button = st.button('提交', key=f"{key}_{label}_submit")
        cancel_button = st.button('取消', key=f"{key}_{label}_cancel")

    with main_st_column:
        col_desc = connection.get_table_column_desc()
        table_name = connection.get_table_name()
        form = dict()
        for col, column_info in col_desc.items():
            # key:
            col_key = f"{key}_{col}"

            # label:
            if (table_name in global_column_translations) and (col in global_column_translations[table_name]):
                col_label = global_column_translations[table_name][col]
            elif column_info['comment']:
                col_label = column_info['comment']
            else:
                col_label = col

            # default:
            if not selected_instance.id:
                default = column_info['default']
            else:
                default = getattr(selected_instance, col)

            if col in ignore:
                continue
            else:
                if column_info['foreign_key']:
                    foreign_key_table_col_name = list(column_info['foreign_key'])[0].target_fullname
                    foreign_Connection = foreign_Connections[foreign_key_table_col_name]

                    foreign_connection = foreign_Connection()
                    all_foreign_instances = foreign_connection.all()
                    foreign_label = foreign_connection.get_table_alias()
                    selected_foreign_instance = main_st_column.selectbox(label=f'选择{foreign_label}',
                                                                         options=all_foreign_instances,
                                                                         key=f"选择{label}_with_{foreign_label}",
                                                                         format_func=lambda x: foreign_Connection.make_label(x))
                    if selected_foreign_instance:
                        col_input = getattr(selected_foreign_instance, foreign_key_table_col_name.split('.')[1])
                    else:
                        col_input = None

                elif column_info['type'] == 'date':
                    if not default:
                        default = datetime.datetime.now().date()
                    col_input = main_st_column.date_input(label=col_label,
                                                          value=default,
                                                          key=col_key)
                elif column_info['type'] == 'datetime':
                    if not default:
                        default = datetime.datetime.now()
                    col_input = main_st_column.date_input(label=col_label,
                                                          value=default,
                                                          key=col_key)
                elif column_info['type'] == 'bool':
                    if not default:
                        default = False
                    col_input = main_st_column.checkbox(label=col_label,
                                                        value=default,
                                                        key=col_key)
                elif column_info['type'] in ['int', 'float']:
                    if not default:
                        col_input = main_st_column.number_input(label=col_label,
                                                                key=col_key)
                    else:
                        col_input = main_st_column.number_input(label=col_label,
                                                                value=default,
                                                                key=col_key)

                    if column_info['type'] == 'int':
                        col_input = int(col_input)
                    else:
                        col_input = float(col_input)
                elif column_info['type'] == 'choice':
                    choices = column_info['choices']
                    col_input = main_st_column.selectbox(label=col_label,
                                                         options=choices,
                                                         index=0,
                                                         key=col_key)
                else:  # str
                    if not default:
                        col_input = main_st_column.text_input(label=col_label,
                                                              key=col_key)
                    else:
                        col_input = main_st_column.text_input(label=col_label,
                                                              value=default,
                                                              key=col_key)

            form[col] = col_input

        if submit_button:
            for col, col_input in form.items():
                if (not col_desc[col]['nullable']) and (not form[col]):
                    main_st_column.error(f'字段<{col_desc[col]["comment"]}>不能为空。')
                    st.stop()

            if not selected_instance.id:  # new
                connection.add_by_dict(form)
                connection.close()
            else:
                selected_instance = connection.query_by_id(id_=selected_instance.id)
                for col, value in form.items():
                    setattr(selected_instance, col, value)
                connection.commit()
                connection.close()

            main_st_column.success(f'成功提交')

        elif cancel_button:
            st.stop()