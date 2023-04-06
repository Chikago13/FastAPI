from typing import Optional
from sqlmodel import SQLModel, Session, create_engine, Field, select, insert
from db2 import Manufacturers, ManufacturersStorehouses, Sweets, SweetsTypes, Storehouses, UserToken,ModelUser
from pydantic import BaseModel  
import json, sys
import datetime
from utils import Utils


utils = Utils()

# engine.connect()

# print(engine)

class DBconnect:
    
    engine = create_engine('postgresql://alex:12345@localhost/mybase')




    # def __new__(cls):
    #     if not hasattr(cls, 'instens'):
    #         cls.instens = super(DBconnect, cls).__new__(cls)
    #         return cls.instens
        
    def convert_json(self, res):
        if isinstance(res, list):
            user_json = []
            for i in res:
                if hasattr(i, 'production_date' or 'expiration_date'):
                    i.production_date, i.expiration_date = utils.convert_datetime_str(i.production_date), utils.convert_datetime_str(i.expiration_date)
                json_data = json.dumps(i.dict(), ensure_ascii=False).encode('utf8')
                user_js = json.loads(json_data.decode('utf8'))
                user_json.append(user_js)
            return user_json
        if hasattr(res, 'production_date' or 'expiration_date'):
            res.production_date, res.expiration_date = utils.convert_datetime_str(res.production_date), utils.convert_datetime_str(res.expiration_date)
        json_data = json.dumps(res.dict(), ensure_ascii=False).encode('utf8')
        user_json = json.loads(json_data.decode('utf8'))
        print(user_json)
        return user_json

        # json_data = json.dumps(res, indent=4, default=str, ensure_ascii=False)
        # user_json = json.loads(json_data)
        # print(json_data)
        # return user_json

        # json_data = json.dumps(res, indent=4, default=str, ensure_ascii=False)
        # json_res = json_data.encode('utf-8').decode('unicode_escape')
        # user_json = json.loads(json_res)
        # print(user_json)
        # return user_json
        # res_dic = res.json()
        # res_dic = json.dumps(res.dict(), ensure_ascii=False).encode('utf8')
        # res_json = json.loads(res_dic.decode('utf8'))
        # # return res_json
        # reload(sys)
        # sys.setdefaultencoding('utf-8')
        # print(res_json)
        # res_dic = [ i.__dict__ for i in res]
        # json_data = json.dumps(res_dic)
        # print(json_data)
        # return res_json
    

    
    def select_all(self, model):
        try:
            with Session(self.engine) as session:
                try:
                    statement = select(model)
                    resalt = session.exec(statement).all()
                    return self.convert_json(resalt)
                except Exception as e:
                    print(e)
                    return False
        except Exception as e:
            return False
        
    def select(self, model, id):
        try:
            with Session(self.engine) as session:
                try:
                    statement = select(model).where(model.id == id)
                    resalt = session.exec(statement).one_or_none()
                    # print(resalt, type(resalt))
                    if resalt:
                        if hasattr(resalt, 'production_date' or 'expiration_date'):
                            resalt.production_date, resalt.expiration_date = utils.convert_datetime_str(resalt.production_date), utils.convert_datetime_str(resalt.expiration_date)
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
                session.refresh(field)
                return True, '', field.id
            except Exception as e:
                return False, e, ''
            
            
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
                    if model == Sweets:
                        upd.name, upd.cost, upd.weight, upd.manufacturer_id, upd.production_date, upd.expiration_date, upd.with_sugar, upd.requires_freezing, upd.sweets_types_id = value["name"], value['cost'], value['weight'], value['manufacturer_id'], value['production_date'], value['expiration_date'], value['with_sugar'], value['requires_freezing'], value['sweets_types_id']
                    elif model == Manufacturers:
                        upd.name, upd.phone, upd.adress, upd.city, upd.country=value['name'], value['phone'], value['adress'], value['city'], value['country']
                    elif model == Storehouses:
                        upd.name,upd.adress, upd.city, upd.country=value['name'], value['adress'], value['city'], value['country']
                    elif model == ManufacturersStorehouses:
                        upd.storehouses_id, upd.manufacturers_id = value['storehouses_id'], value['manufacturers_id']
                    else:
                        model == SweetsTypes
                        upd.name = value['name']
                    session.add(upd)
                    session.commit()
                    session.refresh(upd)
                    return True, ''
                return False, "id is not found "
            except Exception as e:
                return False, e
            



# val = {
#     "id":999,
#     "name": "Nats", 
#     "cost": "250",
#     "weight": "1",
#     "manufacturer_id": 3,
#     "production_date": "2023-01-24",
#     "expiration_date": "2023-01-24",
#     "with_sugar":True,
#     "requires_freezing":False,
#     "sweets_types_id": 2

# }


# cveri = DBconnect()
# print(cveri.select_all(Sweets))
# print(cveri.isnsert(ModelUser(name='Helen', password='3242')))

# print(cveri.select(Manufacturers, Manufacturers.name, 'Трино'))
# man = Manufacturers(id = 1, name= 'Мишаня', phone='75258899771', adress='109235, г. Москва, Проектируемый проезд, д.15', city='Moscow', country='Russia')
# print(cveri.update_field(Manufacturers, man.id, 'name', 'Мишка3'))

# print(cveri.select(Sweets, 1, Sweets.id))