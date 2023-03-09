from typing import Optional
from sqlmodel import SQLModel, Session, create_engine, Field, select, insert
from db2 import Manufacturers, ManufacturersStorehouses, Sweets, SweetsTypes, Storehouses
from pydantic import BaseModel  



# engine.connect()

# print(engine)

class DBconnect:
    
    engine = create_engine('postgresql://alex:12345@localhost/mybase')
    
    def select_all(self, model):
        with Session(self.engine) as session:
            statement = select(model)
            resalt = session.exec(statement).all()
            return resalt
        
    def select(self, model, param, fld):
        with Session(self.engine) as session:
            statement = select(model).where(fld == param)
            resalt = session.exec(statement).all()
            return resalt
        
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






cveri = DBconnect()
print(cveri.select(Manufacturers, Manufacturers.name, 'Трино'))