from streamlit_rental.data_models import create_Session
from streamlit_rental.configs import STATE_DICT


Session = create_Session(db_path=STATE_DICT['configs']['app_db_path'])


class Connection(object):
    def __init__(self, orm):
        self.session = None
        self.orm = orm

    def create_session(self):
        self.session = Session()

    def instanate_orm(self, **kwargs):
        return self.orm(**kwargs)

    def add(self, *instances):
        for instance in instances:
            if isinstance(instance, self.orm):
                self.session.add(instance)
            else:
                raise TypeError(f"instance {instance} of type {type(instance)} is not an instance of {self.orm}.")

        self.commit()

    def flush(self):
        self.session.flush()

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()

