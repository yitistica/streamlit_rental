from streamlit_rental.data_models.models import ContractTemplate, Regularities, Terms
from streamlit_rental.rental.connections import Connection
from streamlit_rental.rental.regularities import COL_TRANSLATION
from sqlalchemy import desc

import json
import pandas as pd


class ContractTemplateConnection(Connection):

    def __init__(self):
        super().__init__(orm=ContractTemplate)

    def all_titles(self):
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

    @staticmethod
    def convert_dicts_to_df(regularities_set_str):
        regularities_set_dict = RegularitiesConnection.convert_set_str_to_dicts(regularities_set_str)
        df = pd.DataFrame(regularities_set_dict)
        df = df.rename(columns=COL_TRANSLATION)
        return df


class TermsConnection(Connection):

    def __init__(self):
        super().__init__(orm=Terms)

    def query_by_id(self, id_):
        terms = self.session.query(self.orm).filter(self.orm.id == id_).first()

        return terms

    def all(self):
        all_instances = []
        for instance in self.session.query(self.orm).order_by(desc(self.orm.id)):
            all_instances.append(instance)

        self.session.close()
        return all_instances

    def all_titles(self):
        all_titles = []
        for info_tuple in self.session.query(Terms.id, Terms.title).\
                order_by(desc(Terms.create_time)):
            all_titles.append(info_tuple)

        self.session.close()
        return all_titles

    @staticmethod
    def make_label(instance):
        if not instance.id:
            return '新合同条款'
        elif instance.id and instance.title:
            return f"{instance.id}. {instance.title}"
        elif instance.title:
            return instance.title
        else:
            return instance.id
