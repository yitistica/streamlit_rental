from streamlit_rental.data_models import create_Session
from streamlit_rental.configs import STATE_DICT
from sqlalchemy.inspection import inspect
from sqlalchemy import types
from sqlalchemy_utils import ChoiceType


def Session_factory():
    STATE_DICT['Session'] = create_Session(db_path=STATE_DICT['configs']['app_db_path'])


def get_column_type(sqltype):
    if isinstance(sqltype, types.Float):
        return 'float'
    elif isinstance(sqltype, types.String):
        return 'str'
    elif isinstance(sqltype, types.Integer):
        return 'int'
    elif isinstance(sqltype, types.Date):
        return 'date'
    elif isinstance(sqltype, types.DateTime):
        return 'datetime'
    elif isinstance(sqltype, types.Boolean):
        return 'bool'
    elif isinstance(sqltype, ChoiceType):
        return 'choice'
    else:
        return None


class Connection(object):
    def __init__(self, orm):
        self._session = None
        self.orm = orm

    @property
    def session(self):
        if self._session is None:
            self.create_session()
        return self._session

    def get_columns(self):
        return [column.name for column in inspect(self.orm).c]

    def get_table_column_desc(self):
        mapper = inspect(self.orm).c

        desc_dict = dict()
        for column in mapper:
            desc_dict[column.name] = dict()
            desc_dict[column.name]['type'] = get_column_type(column.type)
            desc_dict[column.name]['nullable'] = column.nullable
            desc_dict[column.name]['default'] = column.default.arg if column.default else None
            desc_dict[column.name]['choices'] = [choice[0] for choice in column.type.choices] \
                if desc_dict[column.name]['type'] == 'choice' else None
            desc_dict[column.name]['comment'] = column.comment
            desc_dict[column.name]['foreign_key'] = column.foreign_keys

        return desc_dict

    def get_table_name(self):
        return self.orm.__tablename__

    def get_table_alias(self):
        return self.orm.__table_args__['comment']

    def create_session(self):
        self._session = STATE_DICT['Session']()

    def instanate_orm(self, **kwargs):
        return self.orm(**kwargs)

    def add(self, *instances):
        for instance in instances:
            if isinstance(instance, self.orm):
                self.session.add(instance)
            else:
                raise TypeError(f"instance {instance} of type {type(instance)} is not an instance of {self.orm}.")

        self.commit()

    def add_by_dict(self, kwargs):
        instance = self.instanate_orm(**kwargs)
        self.add(instance)

    def flush(self):
        self.session.flush()

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()

