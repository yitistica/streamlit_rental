import streamlit as st
from streamlit_rental.rental.customer import CustomerConnection
import datetime


def _individual_customer_card():
    pass


def add_customer_section():
    my_expander = st.beta_expander("增加住户", expanded=False)
    with my_expander:
        c1, c2, c3, c4 = st.beta_columns((2, 1, 3, 1))

        with c1:
            all_customers = CustomerConnection().all_customer_info()
            new_customer = CustomerConnection().instanate_orm()
            all_customers.insert(0, new_customer)

            selected_customer = st.selectbox(label='选择住户',
                                             options=all_customers, key=f"选择住户",
                                             format_func=lambda customer: CustomerConnection.simplify_names(
                                                 id_=customer.id,
                                                 surname=customer.surname,
                                                 given_name=customer.given_name,
                                                 alias=customer.alias))

            submit_button = st.button('修改/添加', key=f"录入或修改新住户")
            cancel_button = st.button('取消', key=f"取消录入或修改新用户")

        with c3:
            st.markdown("#### 基本信息")
            alias = st.text_input(label='称呼', value=selected_customer.alias if selected_customer.alias else '',
                                  key='增加住户_称呼')
            st.markdown("####")
            surname = st.text_input(label='姓', value=selected_customer.surname if selected_customer.surname else '',
                                    key='增加住户_姓')
            given_name = st.text_input(label='名', value=selected_customer.given_name if selected_customer.given_name else '',
                                       key='增加住户_名')
            nid = st.text_input(label='身份证', value=selected_customer.nid if selected_customer.nid else '',
                                key='增加住户_身份证')
            st.markdown("####")
            st.markdown("#### 联系方式")
            primary_contact_no = st.text_input(label='主联系号码', value=selected_customer.primary_contact_no \
                if selected_customer.primary_contact_no else '', key='增加住户_主联系号码')
            supplementary_contact_no = st.text_input(label='次联系号码', value=selected_customer.supplementary_contact_no \
                if selected_customer.supplementary_contact_no else '', key='增加住户_次联系号码')
            wechat_account = st.text_input(label='微信联系', value=selected_customer.wechat_account \
                                           if selected_customer.wechat_account else '', key='增加住户_微信联系')
            alipay_account = st.text_input(label='支付宝联系', value=selected_customer.alipay_account \
                if selected_customer.alipay_account else '', key='增加住户_支付宝联系')

            if submit_button:
                repeated_customer = CustomerConnection().query_by_nid(nid)
                if repeated_customer and (selected_customer.id != repeated_customer.id):
                    st.error(f"身份证<{repeated_customer.nid}>重复。")

                if not CustomerConnection.check_nid(nid):
                    st.error(f"身份证有误。")

                elif (alias is not None) and (len(alias) < 3):
                    st.error(f"称呼<{alias}>过短。")

                elif (surname is None) or (len(surname) == 0):
                    st.error(f"姓<{surname}>不合规。")

                elif (given_name is None) or (len(given_name) == 0):
                    st.error(f"名<{given_name}>不合规。")

                elif primary_contact_no is None:
                    st.error(f"主联系号码 <{primary_contact_no}>不合规。")

                else:
                    if not selected_customer.id:
                        new_customer.alias = alias
                        new_customer.surname = surname
                        new_customer.given_name = given_name
                        new_customer.nid = nid
                        new_customer.date_of_birth = CustomerConnection.get_birth_date(nid=nid)
                        new_customer.gender = CustomerConnection.get_gender(nid=nid)
                        new_customer.primary_contact_no = primary_contact_no
                        new_customer.supplementary_contact_no = supplementary_contact_no
                        new_customer.wechat_account = wechat_account
                        new_customer.alipay_account = alipay_account
                        new_customer.create_time = datetime.datetime.now()
                        CustomerConnection().add(new_customer)
                    else:
                        connection = CustomerConnection()
                        selected_customer = connection.query_by_id(id_=selected_customer.id)  # replaced;
                        selected_customer.alias = alias
                        selected_customer.surname = surname
                        selected_customer.given_name = given_name
                        selected_customer.nid = nid
                        selected_customer.date_of_birth = CustomerConnection.get_birth_date(nid=nid)
                        selected_customer.gender = CustomerConnection.get_gender(nid=nid)
                        selected_customer.primary_contact_no = primary_contact_no
                        selected_customer.supplementary_contact_no = supplementary_contact_no
                        selected_customer.wechat_account = wechat_account
                        selected_customer.alipay_account = alipay_account
                        selected_customer.create_time = datetime.datetime.now()
                        connection.commit()
                        connection.close()

                    st.success(f'成功提交')

            elif cancel_button:
                st.stop()


def main():

    # add customer
    add_customer_section()




