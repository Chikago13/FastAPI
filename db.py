from sqlalchemy import Boolean, Column, Date, Identity, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Manufacturers(Base):
    __tablename__ = 'manufacturers'
    __table_args__ = {'comment': 'Компании производители', 'schema': 'public'}

    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    phone = Column(String)
    adress = Column(String)


class ManufacturersStorehouses(Base):
    __tablename__ = 'manufacturers_storehouses'
    __table_args__ = {'comment': 'Связь компании производителя и склада', 'schema': 'public'}

    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    storehouses_id = Column(Integer, nullable=False)
    manufacturers_id = Column(Integer, nullable=False)


class Storehouses(Base):
    __tablename__ = 'storehouses'
    __table_args__ = {'comment': 'Склады', 'schema': 'public'}

    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    adress = Column(String)


class Sweets(Base):
    __tablename__ = 'sweets'
    __table_args__ = {'comment': 'Записи о сладостях', 'schema': 'public'}

    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name = Column(String, nullable=False)
    cost = Column(String, nullable=False)
    weight = Column(String, nullable=False)
    manufacturer_id = Column(Integer, nullable=False)
    production_date = Column(Date, nullable=False)
    expiration_date = Column(Date, nullable=False)
    sweets_types_id = Column(Integer)
    with_sugar = Column(Boolean)
    requires_freezing = Column(Boolean)


class SweetsTypes(Base):
    __tablename__ = 'sweets_types'
    __table_args__ = {'comment': 'Виды сладостей', 'schema': 'public'}

    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name = Column(String, nullable=False)
