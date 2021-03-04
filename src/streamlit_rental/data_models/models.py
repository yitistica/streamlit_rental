from sqlalchemy_utils import ChoiceType
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Enum

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


class Apartment(Base):
    __tablename__ = 'apartment'
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


class RegularityType(Base):
    __tablename__ = 'regularity'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    type = Column('type', String, nullable=False)
    name = Column('name', String, nullable=False)


class Terms(Base):

    __tablename__ = 'terms'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    templates = Column(String, ForeignKey('ContractTemplate.id'))
    prvisions = Column('prvisions', String, nullable=True)
    # regularities, json str: {regularity_id: set}, this is used to calculate monthly price;
    regularities = Column('regularities', String, nullable=False)



