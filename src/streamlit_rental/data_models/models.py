from sqlalchemy_utils import ChoiceType
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum

from streamlit_rental.data_models.declarative import Base


class Person(Base):
    __tablename__ = 'person'
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]

    GENDERS = tuple(i[0] for i in GENDER_CHOICES)
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    surname = Column('surname', String, nullable=False)
    given_name = Column('given_name', String, nullable=False)
    gender = Column('gender', ChoiceType(GENDER_CHOICES, impl=Enum(*GENDERS, name='gender')),
                    default='female', nullable=False)
    alias = Column('alias', String, nullable=True)


class Owner(Person):
    __tablename__ = 'owner'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)


class Manager(Person):
    __tablename__ = 'manager'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    access_key = Column('access_key', String, nullable=False)
    manage_key = Column('manage_key', String, nullable=False)


class Customer(Person):
    __tablename__ = 'customer'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    nid = Column('nid', String, nullable=False)
    date_of_birth = Column('date of birth', DateTime, nullable=False)


class Property(Base):
    __tablename__ = 'property'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    address = Column('address', String, nullable=False)
    alias = Column('alias', String, nullable=True)


class RentalUnit(Base):
    __tablename__ = 'rental_unit'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    unit = Column('unit', String, nullable=False)
    property = Column(String, ForeignKey('property.id'))
    owner = Column(String, ForeignKey('owner.id'))
    manager = Column(String, ForeignKey('manager.id'))


class ContractTemplate(Base):
    __tablename__ = 'contract_template'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    create_time = Column('create_time', DateTime, nullable=False)
    update_time = Column('update_time', DateTime, nullable=False)
    create_author = Column(String, ForeignKey('person.id'))
    update_author = Column(String, ForeignKey('person.id'))
    template_title = Column('template_title', String, nullable=False)
    template_content = Column('template_content', String, nullable=False)


class Regularities(Base):
    __tablename__ = 'regularities'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    type = Column('type', String, nullable=False)
    items = Column('items', String, nullable=True)


class Terms(Base):

    __tablename__ = 'terms'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    templates = Column(String, ForeignKey('contract_template.id'))
    provisions = Column('provisions', String, nullable=True)
    regularities = Column(Integer, ForeignKey('regularities.id'))  # format;


class Contract(Base):
    __tablename__ = 'contract'

    STATUS_CHOICES = [
        ('not signed', 'Not Signed'),
        ('active', 'Active'),
        ('terminated', 'Terminated'),
        ('expired', 'Expired'),
    ]

    STATUSES = tuple(i[0] for i in STATUS_CHOICES)

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    rental_id = Column(Integer, ForeignKey('rental_unit.id'))
    primary_customer = Column(Integer, ForeignKey('customer.id'))
    start_date = Column('start_date', DateTime, nullable=False)
    end_date = Column('end_date', DateTime, nullable=False)
    terms = Column(Integer, ForeignKey('terms.id'))
    issuer = Column(Integer, ForeignKey('manager.id'))
    status = Column('status', ChoiceType(STATUS_CHOICES, impl=Enum(*STATUSES, name='gender')),
                    default='not signed', nullable=False)


class Session(Base):
    __tablename__ = 'session'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    session_date = Column('session_date', DateTime, nullable=False)
    contract_id = Column(String, ForeignKey('contract.id'))
    manager = Column(String, ForeignKey('manager.id'))


class Usage(Base):
    __tablename__ = 'usage'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey('session.id'))
    item = Column('item', String, nullable=False)
    value = Column('value', Float, nullable=False)
    start_date = Column('start_date', DateTime, nullable=False)
    end_date = Column('end_date', DateTime, nullable=False)


class Billables(Base):
    __tablename__ = 'billables'

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('rolled over', 'Rolled Over'),
        ('delayed', 'Delayed'),
        ('forgiven', 'Forgiven'),
        ('bad', 'Bad'),
    ]
    STATUSES = tuple(i[0] for i in STATUS_CHOICES)

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey('session.id'))
    item = Column('item', String, nullable=False)
    value = Column('value', Float, nullable=False)
    status = Column('status', ChoiceType(STATUS_CHOICES, impl=Enum(*STATUSES, name='gender')),
                    default='pending', nullable=False)
    remarks = Column('remarks', String, nullable=False)
