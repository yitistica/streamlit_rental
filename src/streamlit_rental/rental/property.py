from streamlit_rental.data_models.models import Owner, Property
from streamlit_rental.rental.connections import Connection
from sqlalchemy import desc


class OwnerConnection(Connection):

    def __init__(self):
        super().__init__(orm=Owner)

    def all(self):
        all_owners = []
        for owner in self.session.query(Owner).order_by(desc(Owner.id)):
            all_owners.append(owner)

        self.session.close()
        return all_owners

    def query_by_id(self, id_):
        owner = self.session.query(Owner).filter(Owner.id == id_).first()

        return owner

    @staticmethod
    def make_label(instance):
        if not instance.id:
            return '新所有人'
        elif instance.alias:
            return instance.alias
        elif instance.given_name:
            return f"{instance.id}. {instance.given_name}"
        elif instance.surname:
            return f"{instance.id}. {instance.surname}"
        else:
            return instance.id


class PropertyConnection(Connection):

    def __init__(self):
        super().__init__(orm=Property)

    def all(self):
        all_properties = []
        for prop in self.session.query(Property).order_by(desc(Property.id)):
            all_properties.append(prop)

        self.session.close()
        return all_properties

    def query_by_id(self, id_):
        prop = self.session.query(Property).filter(Property.id == id_).first()

        return prop

    @staticmethod
    def make_label(instance):
        if not instance.id:
            return '新产权'
        elif instance.alias:
            return instance.alias
        else:
            return instance.id
