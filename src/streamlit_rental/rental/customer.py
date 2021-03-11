from streamlit_rental.data_models.models import Customer, Contract
from streamlit_rental.rental.connections import Connection
from sqlalchemy import desc

import datetime


class CustomerConnection(Connection):

    def __init__(self):
        super().__init__(orm=Customer)

    def all(self):
        all_customers = []
        for customer in self.session.query(Customer).order_by(desc(Customer.id)):
            all_customers.append(customer)

        self.session.close()
        return all_customers

    def query_by_id(self, id_):
        customer = self.session.query(Customer).filter(Customer.id == id_).first()

        return customer

    def query_by_nid(self, nid):
        customer = self.session.query(Customer).filter(Customer.nid == nid).first()
        return customer

    def get_contracts(self, customer_id, filter_status=None):
        if isinstance(filter_status, str):
            filter_status = [filter_status]

        if not filter_status:
            query = self.session.query(Contract).filter_by(Contract.customer_id == customer_id).all()
        else:
            query = self.session.query(Contract).filter_by(Contract.customer_id == customer_id,
                                                           Contract.status in filter_status, ).all()

        return query

    @staticmethod
    def check_nid(nid):
        if len(nid) != 18:
            return False

        if not CustomerConnection.get_birth_date(nid=nid):
            return False

        return True

    @staticmethod
    def get_birth_date(nid):
        birthday_str = nid[6: 14]
        try:
            birth_date = datetime.datetime.strptime(birthday_str, "%Y%m%d").date()
        except ValueError:
            birth_date = None

        return birth_date

    @staticmethod
    def get_gender(nid):
        if int(nid[-1]) % 2 == 0:
            return '女'
        else:
            return '男'

    @staticmethod
    def simplify_names(id_, surname, given_name, alias):

        if not id_:
            return "新住户"
        if alias == surname + given_name:
            simplified_name = alias
        elif alias == given_name:
            simplified_name = surname + alias
        else:
            simplified_name = surname + given_name + ' (' + alias + ')'

        return f"{id_}. {simplified_name}"

    @staticmethod
    def make_label(instance):
        return CustomerConnection.simplify_names(id_=instance.id,
                                                 surname=instance.surname,
                                                 given_name=instance.given_name,
                                                 alias=instance.alias)