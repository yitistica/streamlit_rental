from streamlit_rental.data_models.models import Owner
from streamlit_rental.rental.connections import Connection


class OwnerConnection(Connection):

    def __init__(self):
        super().__init__(orm=Owner)
