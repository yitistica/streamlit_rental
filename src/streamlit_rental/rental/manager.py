from streamlit_rental.data_models.models import Manager
from streamlit_rental.rental.connections import Connection


class ManagerConnection(Connection):

    def __init__(self):
        super().__init__(orm=Manager)

    def add_manager(self, **kwargs):
        instance = self.instanate_orm(**kwargs)
        self.add(instance)

