from datetime import date
from typing import Optional

from sqlalchemy import Boolean, Column, Date, Identity, Integer, PrimaryKeyConstraint, String
from sqlmodel import Field, SQLModel

class Manufacturers(SQLModel, table=True):
    __table_args__ = (
        PrimaryKeyConstraint('id', name='manufacturers_pkey'),
        {'comment': 'Компании производители', 'schema': 'public'}
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1)))
    name: str = Field(sa_column=Column('name', String, nullable=False))
    city: str = Field(sa_column=Column('city', String, nullable=False))
    country: str = Field(sa_column=Column('country', String, nullable=False))
    phone: Optional[str] = Field(default=None, sa_column=Column('phone', String))
    adress: Optional[str] = Field(default=None, sa_column=Column('adress', String))


class ManufacturersStorehouses(SQLModel, table=True):
    __tablename__ = 'manufacturers_storehouses'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='manufacturers_storehouses_pkey'),
        {'comment': 'Связь компании производителя и склада', 'schema': 'public'}
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1)))
    storehouses_id: int = Field(sa_column=Column('storehouses_id', Integer, nullable=False))
    manufacturers_id: int = Field(sa_column=Column('manufacturers_id', Integer, nullable=False))


class Storehouses(SQLModel, table=True):
    __table_args__ = (
        PrimaryKeyConstraint('id', name='storehouses_pkey'),
        {'comment': 'Склады', 'schema': 'public'}
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1)))
    name: str = Field(sa_column=Column('name', String, nullable=False))
    city: str = Field(sa_column=Column('city', String, nullable=False))
    country: str = Field(sa_column=Column('country', String, nullable=False))
    adress: Optional[str] = Field(default=None, sa_column=Column('adress', String))


class Sweets(SQLModel, table=True):
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sweets_pkey'),
        {'comment': 'Записи о сладостях', 'schema': 'public'}
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1)))
    name: str = Field(sa_column=Column('name', String, nullable=False))
    cost: str = Field(sa_column=Column('cost', String, nullable=False))
    weight: str = Field(sa_column=Column('weight', String, nullable=False))
    manufacturer_id: int = Field(sa_column=Column('manufacturer_id', Integer, nullable=False))
    production_date: date = Field(sa_column=Column('production_date', Date, nullable=False))
    expiration_date: date = Field(sa_column=Column('expiration_date', Date, nullable=False))
    sweets_types_id: Optional[int] = Field(default=None, sa_column=Column('sweets_types_id', Integer))
    with_sugar: Optional[bool] = Field(default=None, sa_column=Column('with_sugar', Boolean))
    requires_freezing: Optional[bool] = Field(default=None, sa_column=Column('requires_freezing', Boolean))


class SweetsTypes(SQLModel, table=True):
    __tablename__ = 'sweets_types'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sweets_types_pkey'),
        {'comment': 'Виды сладостей', 'schema': 'public'}
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1)))
    name: str = Field(sa_column=Column('name', String, nullable=False))
