from pydantic import BaseModel

class Manufacturers(BaseModel):
    id: int
    name: str
    phone: str
    adress: str
    city: str
    country: str

class Storehouses(BaseModel):
    id: int
    name: str
    adress: str
    city: str
    country: str

class Sweets_types(BaseModel):
    id: int
    name: str

class Sweets(BaseModel):
    id: int
    sweets_types: Sweets_types
    name: str
    cost: float
    weight: float
    manufacturers: list=[Manufacturers]
    with_sugar: bool
    requiers_freezing: bool
    production_data: str
    expiration_data: str

