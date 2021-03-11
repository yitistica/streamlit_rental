import streamlit as st
import datetime

from streamlit_rental.rental.contracts import ContractConnection, CustomerConnection, TermsConnection, \
    RentalUnitConnection
from streamlit_rental.rental.contract_builder import RegularitiesConnection
from streamlit_rental.pages.utils.display_components import convert_a_dict_to_table
from streamlit_ace import st_ace

ace_setting = {'placeholder': "请拟定合同内容",
               'language': "markdown",
               'theme': 'github',
               'keybinding': 'sublime',
               'tab_size': 4,
               }


_default_provision = ''

_saved_provision = [_default_provision]


def add_new_contract():
    my_expander = st.beta_expander("制定新合同", expanded=True)
    with my_expander:
        c1, c2, c3 = st.beta_columns((1.5, 4, 6))

        with c1:
            # customer:
            customer_connection = CustomerConnection()
            all_customers = customer_connection.all()  # with all method

            selected_customer = st.selectbox(label=f'选择客户',
                                             options=all_customers, key=f"选择客户(合同)",
                                             format_func=lambda x: CustomerConnection.make_label(x))

            # rental unit:
            rental_unit_connection = RentalUnitConnection()
            all_rental_units = rental_unit_connection.all()  # with all method

            selected_rental_unit = st.selectbox(label=f'选择住房单元',
                                                options=all_rental_units, key=f"选择住房单元(合同)",
                                                format_func=lambda x: RentalUnitConnection.make_label(x))

            # terms:
            terms_connection = TermsConnection()
            all_terms = terms_connection.all()  # with all method

            selected_terms = st.selectbox(label=f'选择合同条款',
                                          options=all_terms, key=f"选择合同条款(合同)",
                                          format_func=lambda x: TermsConnection.make_label(x))

            # status
            choices = ContractConnection().get_table_column_desc()['status']['choices']
            selected_status = st.selectbox(label=f'初始合同状态',
                                           options=choices, key=f"选择初始合同状态(合同)",)

            # date:
            now = datetime.date.today()
            select_start_date = st.date_input('合同开始日期', value=now, key=f"选择合同开始时间")
            select_end_date = st.date_input('合同结束日期', value=now + datetime.timedelta(days=365),
                                            key=f"选择合同结束时间")

            submit_button = st.button('制造', key=f"合同制作_submit")
            cancel_button = st.button('取消', key=f"合同制作_cancel")

        with c2:
            if selected_customer:
                st.markdown("#### 客户信息")

                customer_info = {}
                selected_customer = customer_connection.query_by_id(id_=selected_customer.id)
                customer_info['客户编号'] = selected_customer.id
                customer_info['客户姓名'] = f"{selected_customer.surname} {selected_customer.given_name}"
                customer_info['身份证'] = selected_customer.nid
                customer_info['主联系号码'] = selected_customer.primary_contact_no
                customer_info['紧急联系人'] = selected_customer.emergency_contact
                customer_info['紧急联系号码'] = selected_customer.emergency_contact_no

                customer_info_df = convert_a_dict_to_table(customer_info)
                st.table(customer_info_df)

            if selected_rental_unit:
                st.markdown("#### 房屋信息")

                rental_unit_info = {}
                selected_rental_unit = rental_unit_connection.query_by_id(id_=selected_rental_unit.id)
                rental_unit_info['单元编号'] = selected_rental_unit.id
                rental_unit_info['单元号'] = selected_rental_unit.unit
                rental_unit_info['单元楼'] = selected_rental_unit.property.alias
                rental_unit_info['地址'] = selected_rental_unit.property.address

                rental_unit_info_df = convert_a_dict_to_table(rental_unit_info)
                st.table(rental_unit_info_df)

            if selected_terms:
                st.markdown("#### 收费信息")
                selected_terms = terms_connection.query_by_id(id_=selected_terms.id)
                regularities_set_df = RegularitiesConnection.convert_dicts_to_df(selected_terms.regularities.set)
                regularities_set_df = regularities_set_df[regularities_set_df['价格'] > 0].reset_index(drop=True)
                st.table(regularities_set_df)

            st.markdown('#### 其它规定')
            provisions = st_ace(_saved_provision[0], **ace_setting)

        with c3:
            if selected_terms:
                selected_terms = terms_connection.query_by_id(id_=selected_terms.id)
                st.markdown(selected_terms.template.content)

            st.markdown('#### 其它规定')
            st.markdown(provisions)

        if submit_button:
            if selected_customer and selected_rental_unit and selected_terms:
                contract_connection = ContractConnection()
                contract = contract_connection.instanate_orm()

                contract.customer_id = selected_customer.id
                contract.rental_id = selected_rental_unit.id
                contract.terms_id = selected_terms.id
                contract.provisions = provisions
                contract.status = selected_status
                contract.start_date = select_start_date
                contract.end_date = select_end_date

                contract_connection.add(contract)
                contract_connection.close()
                _saved_provision[0] = ''
                c1.success(f'成功提交')
            else:
                c1.error(f"请选择必选项。")
        elif cancel_button:
            st.stop()


def main():
    # add new contract
    add_new_contract()



