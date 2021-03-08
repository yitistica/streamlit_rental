from streamlit_rental.data_models.models import ContractTemplate, Regularities, Terms
from streamlit_rental.rental.connections import Connection
from sqlalchemy import desc


class ContractTemplateConnection(Connection):

    def __init__(self):
        super().__init__(orm=ContractTemplate)

    def all_templates(self):
        all_templates = []
        for info_tuple in self.session.query(ContractTemplate.id, ContractTemplate.template_title).\
                order_by(desc(ContractTemplate.update_time)):
            all_templates.append(info_tuple)

        self.session.close()
        return all_templates

    def query_by_template_id(self, id_):
        template = self.session.query(ContractTemplate).filter(ContractTemplate.id == id_).first()

        return template


class RegularitiesConnection(Connection):

    def __init__(self):
        super().__init__(orm=Regularities)


class TermsConnection(Connection):

    def __init__(self):
        super().__init__(orm=Terms)

