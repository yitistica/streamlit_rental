from streamlit_rental.data_models.models import ContractTemplate, Regularities, Terms
from streamlit_rental.rental.connections import Connection
from sqlalchemy import desc

import json

class ContractTemplateConnection(Connection):

    def __init__(self):
        super().__init__(orm=ContractTemplate)

    def all_template_titles(self):
        all_templates = []
        for info_tuple in self.session.query(ContractTemplate.id, ContractTemplate.title).\
                order_by(desc(ContractTemplate.create_time)):
            all_templates.append(info_tuple)

        self.session.close()
        return all_templates

    def query_by_id(self, id_):
        template = self.session.query(ContractTemplate).filter(ContractTemplate.id == id_).first()

        return template


class RegularitiesConnection(Connection):

    def __init__(self):
        super().__init__(orm=Regularities)

    def all_titles(self):
        all_regularities_set = []
        for info_tuple in self.session.query(Regularities.id, Regularities.title).\
                order_by(desc(Regularities.create_time)):
            all_regularities_set.append(info_tuple)

        self.session.close()
        return all_regularities_set

    def query_by_id(self, id_):
        regularities_set = self.session.query(Regularities).filter(Regularities.id == id_).first()

        return regularities_set

    @staticmethod
    def convert_set_str_to_dicts(regularities_set_str):
        return json.loads(regularities_set_str)

    @staticmethod
    def convert_dicts_to_set_str(regularities_set_dict):
        return json.dumps(regularities_set_dict)


class TermsConnection(Connection):

    def __init__(self):
        super().__init__(orm=Terms)

