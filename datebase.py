from typing import Optional
from sqlmodel import SQLModel, Session, create_engine, Field, select, insert
from db2 import Manufacturers, ManufacturersStorehouses, Sweets, SweetsTypes, Storehouses
from pydantic import BaseModel  
import json



# engine.connect()

# print(engine)

class DBconnect:
    
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
        
    def select(self, model, id):
        try:
            with Session(self.engine) as session:
                try:
                    statement = select(model).where(model.id == id)
                    resalt = session.exec(statement).one_or_none()
                    if resalt:
                        return self.convert_json(resalt)
                    return False
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
            
    def dlt(self, model, id):
        with Session(self.engine) as session:
            try:
                statement = select(model).where(model.id == id)
                results = session.exec(statement)
                id_dl = results.one()
                session.delete(id_dl)
                session.commit()
                return True, ''
            except Exception as e:
                return False, e
            


    def update_field(self, model, value):
        with Session(self.engine) as session:
            try:
                statement = select(model).where(model.id==value["id"])
                results = session.exec(statement)
                upd = results.one_or_none()
                if upd:
                    upd.name, upd.cost, upd.weight, upd.manufacturer_id, upd.production_date, upd.expiration_date, upd.with_sugar, upd.requires_freezing, upd.sweets_types_id = value["name"], value['cost'], value['weight'], value['manufacturer_id'], value['production_date'], value['expiration_date'], value['with_sugar'], value['requires_freezing'], value['sweets_types_id']
                    session.add(upd)
                    session.commit()
                    session.refresh(upd)
                    return True, ''
                return False, "id is not found "
            except Exception as e:
                return False, e



val = {
    "id":999,
    "name": "Nats", 
    "cost": "250",
    "weight": "1",
    "manufacturer_id": 3,
    "production_date": "2023-01-24",
    "expiration_date": "2023-01-24",
    "with_sugar":True,
    "requires_freezing":False,
    "sweets_types_id": 2

}


# cveri = DBconnect()
# print(cveri.update_field(Sweets, val))
# # print(cveri.select(Manufacturers, Manufacturers.name, 'Трино'))
# man = Manufacturers(id = 1, name= 'Мишаня', phone='75258899771', adress='109235, г. Москва, Проектируемый проезд, д.15', city='Moscow', country='Russia')
# print(cveri.update_field(Manufacturers, man.id, 'name', 'Мишка3'))

# print(cveri.select(Sweets, 1, Sweets.id))