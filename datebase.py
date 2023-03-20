from typing import Optional
from sqlmodel import SQLModel, Session, create_engine, Field, select, insert
from db2 import Manufacturers, ManufacturersStorehouses, Sweets, SweetsTypes, Storehouses
from pydantic import BaseModel  
import json



# engine.connect()

# print(engine)

class DBconnect:

    def __init__(self, model):
        self.model = model

    
    engine = create_engine('postgresql://alex:12345@localhost/mybase')


    # def __new__(cls):
    #     if not hasattr(cls, 'instens'):
    #         cls.instens = super(DBconnect, cls).__new__(cls)
    #         return cls.instens
        
    def convert_json(self, res):
        res_dic = [ i.__dict__ for i in res]
        # json_data = json.dumps(res_dic)
        # print(json_data)
        return res_dic

    
    def select_all(self, model):
        try:
            with Session(self.engine) as session:
                try:
                    statement = select(model)
                    resalt = session.exec(statement).all()
                    return self.convert_json(resalt)
                except Exception as e:
                    return False
        except Exception as e:
            return False
        
    def select(self, model, param, fld):
        try:
            with Session(self.engine) as session:
                try:
                    statement = select(model).where(fld == param)
                    resalt = session.exec(statement).all()
                    return self.convert_json(resalt)
                except Exception as e:
                    return False
        except:
            return False
        
    def isnsert(self, field):
        with Session(self.engine) as session:
            try:
                session.add(field)
                session.commit()
                return True, ''
            except Exception as e:
                return False, e
            
    def dlt(self, model, field, param):
        with Session(self.engine) as session:
            try:
                statement = select(model).where(field == param)
                results = session.exec(statement)
                return True, ''
            except Exception as e:
                return False, e
            


    def update_field(self, model, id, value):
        with Session(self.engine) as session:
            try:
                statement = select(model).where(model.id==id, model.id == value.id)
                results = session.exec(statement)
                upd = results.one()
                upd.id = value.id
                upd.name = value.name
                upd.cost = value.cost
                upd.weight= value.weight
                upd.manufacturer_id = value.manufacturer_id
                upd.production_date = value.production_date
                upd.expiration_date =value.expiration_date
                upd.with_sugar = value.with_sugar
                upd.requires_freezing = value.requires_freezing
                upd.sweets_types_id =value.sweets_types_id
                session.add(upd)
                session.commit()
                session.refresh(upd)
                return True, ''
            except Exception as e:
                return False, e






# cveri = DBconnect()
# print(cveri.update_field(Sweets, 5, name = "cost", val="500"))
# # print(cveri.select(Manufacturers, Manufacturers.name, 'Трино'))
# man = Manufacturers(id = 1, name= 'Мишаня', phone='75258899771', adress='109235, г. Москва, Проектируемый проезд, д.15', city='Moscow', country='Russia')
# print(cveri.update_field(Manufacturers, man.id, 'name', 'Мишка3'))

# print(cveri.select(Sweets, 1, Sweets.id))