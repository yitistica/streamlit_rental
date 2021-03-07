from streamlit_rental.data_models.models import Customer, Contract
from streamlit_rental.rental.connections import Connection


class ManagerConnection(Connection):

    def __init__(self):
        super().__init__(orm=Customer)

    def get_contracts(self, customer_id, filter_status=None):
        if isinstance(filter_status, str):
            filter_status = [filter_status]

        if not filter_status:
            query = self.session.query(Contract).filter_by(Contract.primary_customer == customer_id).all()
        else:
            query = self.session.query(Contract).filter_by(Contract.primary_customer == customer_id,
                                                           Contract.status in filter_status,).all()

        return query

