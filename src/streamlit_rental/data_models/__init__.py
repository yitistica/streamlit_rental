from streamlit_rental.data_models.models import Customer
from streamlit_rental.data_models.declarative import Base
from sqlalchemy import create_engine
import datetime


def create_lite_engine(db_path, echo=True):
    engine = create_engine(f'sqlite:///{db_path}', echo=echo)
    return engine



engine = create_lite_engine(db_path='C:/Users/yeech/Desktop/streamlit_rental_working_directory/a.db')


Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import sessionmaker


Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

customer = Customer()
customer.surname = 'abc'
customer.given_name = 'de'
customer.nid = 'sasafa'
customer.date_of_birth = datetime.datetime.now()

session.add(customer)
session.commit()
session.close()
