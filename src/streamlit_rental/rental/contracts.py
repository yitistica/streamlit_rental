from streamlit_rental.data_models.models import Contract, RentalUnit, Terms, Customer
from streamlit_rental.rental.connections import Connection
from streamlit_rental.rental.contract_builder import TermsConnection
from streamlit_rental.rental.property import RentalUnitConnection
from streamlit_rental.rental.customer import CustomerConnection
from sqlalchemy import desc


class ContractConnection(Connection):

    def __init__(self):
        super().__init__(orm=Contract)

    def all(self):
        all_ = []
        for contract in self.session.query(Contract).order_by(desc(Contract.id)):
            all_.append(contract)

        self.session.close()
        return all_

    def query_by_id(self, id_):
        contract = self.session.query(Contract).filter(Contract.id == id_).first()

        return contract

    def query_rental_unit_availability(self, rental_id):
        contracts = self.session.query(Contract).filter(Contract.rental_id == rental_id).all()

        if contracts:
            return False
        else:
            return True

    def query_rental_unit(self, rental_id):
        rental_unit = self.session.query(RentalUnit).filter(RentalUnit.id == rental_id).first()

        return rental_unit

    def query_terms_info(self, term_id):
        terms = self.session.query(Terms).filter(Terms.id == term_id).first()
        return terms

    @staticmethod
    def query_all_customers():
        customers = CustomerConnection().all()
        return customers

    @staticmethod
    def query_all_terms():
        terms = TermsConnection().all()
        return terms

    @staticmethod
    def query_all_rental_units():
        units = RentalUnitConnection().all()
        return units

    def init_contract(self, customer_id, rental_id, terms_id, start_date, end_date, provisions, status):
        avaliable = self.query_rental_unit_availability(rental_id=rental_id)

        if not avaliable:
            return False
        else:
            contract = self.orm()
            contract.customer_id = customer_id
            contract.rental_id = rental_id
            contract.terms_id = terms_id
            contract.start_date = start_date
            contract.end_date = end_date
            contract.provisions = provisions if provisions else ''
            contract.status = status

            self.add(contract)
            self.close()
            return True
