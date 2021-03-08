from streamlit_rental.data_models.models import Manager, Owner
from streamlit_rental.rental.connections import Connection


class ManagerConnection(Connection):

    def __init__(self):
        super().__init__(orm=Manager)

    def all_managers(self):
        all_managers = []
        for info_tuple in self.session.query(Manager.id, Manager.alias).all():
            all_managers.append(info_tuple)

        self.session.close()
        return all_managers


class OwnerConnection(Connection):

    def __init__(self):
        super().__init__(orm=Owner)
