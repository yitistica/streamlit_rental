from sqlalchemy_utils import ChoiceType
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum

from streamlit_rental.data_models.declarative import Base


class Person(Base):
    __tablename__ = 'person'
    __table_args__ = {'comment': '人员'}

    GENDER_CHOICES = [
        ('男', '男'),
        ('女', '女')
    ]

    GENDERS = tuple(i[0] for i in GENDER_CHOICES)
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='编号')
    surname = Column('surname', String, nullable=False, comment='姓')
    given_name = Column('given_name', String, nullable=False, comment='名')
    gender = Column('gender', ChoiceType(GENDER_CHOICES, impl=Enum(*GENDERS, name='gender')),
                    default='女', nullable=False, comment='性别')
    alias = Column('alias', String, nullable=True, comment='别称')


class Owner(Person):
    __tablename__ = 'owner'
    __table_args__ = {'comment': '所有者'}

    id = Column(Integer, ForeignKey('person.id'), primary_key=True, comment='编号')


class Manager(Person):
    __tablename__ = 'manager'
    __table_args__ = {'comment': '管理者'}

    id = Column(Integer, ForeignKey('person.id'), primary_key=True, comment='编号')
    access_key = Column('access_key', String, nullable=False, comment='访问权限密码')
    manage_key = Column('manage_key', String, nullable=False, comment='管理权限密码')


class Customer(Person):
    __tablename__ = 'customer'
    __table_args__ = {'comment': '客户'}

    id = Column(Integer, ForeignKey('person.id'), primary_key=True, comment='编号')
    nid = Column('nid', String, nullable=False, comment='身份证明')
    date_of_birth = Column('date of birth', DateTime, nullable=False, comment='生日日期')


class Property(Base):
    __tablename__ = 'property'
    __table_args__ = {'comment': '产权'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='编号')
    address = Column('address', String, nullable=False, comment='地址')
    alias = Column('alias', String, nullable=True, comment='别称')


class RentalUnit(Base):
    __tablename__ = 'rental_unit'
    __table_args__ = {'comment': '单元'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='编号')
    unit = Column('unit', String, nullable=False, comment='单元')
    property = Column(String, ForeignKey('property.id'), comment='产权编号')
    owner = Column(String, ForeignKey('owner.id'), comment='所有者')
    manager = Column(String, ForeignKey('manager.id'), comment='管理者')


class ContractTemplate(Base):
    __tablename__ = 'contract_template'
    __table_args__ = {'comment': '合同模板'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='编号')
    create_time = Column('create_time', DateTime, nullable=False, comment='创建时间')
    update_time = Column('update_time', DateTime, nullable=False, comment='更新时间')
    create_author = Column(String, ForeignKey('manager.id'), comment='创建者')
    update_author = Column(String, ForeignKey('manager.id'), comment='更新作者')
    template_title = Column('template_title', String, nullable=False, comment='标题')
    template_content = Column('template_content', String, nullable=False, comment='内容')


class Regularities(Base):
    __tablename__ = 'regularities'
    __table_args__ = {'comment': '常规项'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='编号')
    type = Column('type', String, nullable=False, comment='常规项类别')
    items = Column('items', String, nullable=True, comment='常规项集')


class Terms(Base):

    __tablename__ = 'terms'
    __table_args__ = {'comment': '条款'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='编号')
    templates = Column(String, ForeignKey('contract_template.id'), comment='合同模板编号')
    provisions = Column('provisions', String, nullable=True, comment='其它規定')
    regularities = Column(Integer, ForeignKey('regularities.id'), comment='常规项编号')  # format;


class Contract(Base):
    __tablename__ = 'contract'
    __table_args__ = {'comment': '合同'}

    STATUS_CHOICES = [
        ('未生效', '未生效'),
        ('生效中', '生效中'),
        ('终止', '终止'),
        ('过期', '过期'),
        ('其它', '其它'),
    ]

    STATUSES = tuple(i[0] for i in STATUS_CHOICES)

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='编号')
    rental_id = Column(Integer, ForeignKey('rental_unit.id'), comment='单元编号')
    primary_customer = Column(Integer, ForeignKey('customer.id'), comment='客户编号')
    start_date = Column('start_date', DateTime, nullable=False, comment='开始时间')
    end_date = Column('end_date', DateTime, nullable=False, comment='结束时间')
    terms = Column(Integer, ForeignKey('terms.id'), comment='条款')
    issuer = Column(Integer, ForeignKey('manager.id'), comment='合同拟定者')
    status = Column('status', ChoiceType(STATUS_CHOICES, impl=Enum(*STATUSES, name='status')),
                    default='无效', nullable=False, comment='状态')


class Session(Base):
    __tablename__ = 'session'
    __table_args__ = {'comment': '管理交互'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='编号')
    session_date = Column('session_date', DateTime, nullable=False, comment='交互开始时间')
    contract_id = Column(String, ForeignKey('contract.id'), comment='合同编号')
    manager = Column(String, ForeignKey('manager.id'), comment='管理者')


class Usage(Base):
    __tablename__ = 'usage'
    __table_args__ = {'comment': '常规使用'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='编号')
    session_id = Column(String, ForeignKey('session.id'), comment='交互编号')
    item = Column('item', String, nullable=False, comment='项目')
    value = Column('value', Float, nullable=False, comment='值')
    start_date = Column('start_date', DateTime, nullable=False, comment='项目对应开始时间')
    end_date = Column('end_date', DateTime, nullable=False, comment='项目对应结束时间')


class Billables(Base):
    __tablename__ = 'billables'
    __table_args__ = {'comment': '计费'}

    STATUS_CHOICES = [
        ('生成', '生成'),
        ('等待支付', '等待支付'),
        ('已付款', '已付款'),
        ('延期', '延期'),
        ('拖欠', '拖欠'),
        ('宽免', '宽免'),
        ('坏账', '坏账'),
    ]
    STATUSES = tuple(i[0] for i in STATUS_CHOICES)

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='编号')
    session_id = Column(String, ForeignKey('session.id'), comment='交互编号')
    item = Column('item', String, nullable=False, comment='计费项目')
    value = Column('value', Float, nullable=False, comment='费用')
    status = Column('status', ChoiceType(STATUS_CHOICES, impl=Enum(*STATUSES, name='status')),
                    default='生成', nullable=False, comment='状态')
    remarks = Column('remarks', String, nullable=True, comment='费用旁注')
