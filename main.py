from fastapi import FastAPI, Response, Path, Query, Body, status, Header, Cookie, Form, Depends, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse, FileResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
import mimetypes, uuid
from pydantic import BaseModel
from datetime import datetime
from datebase import DBconnect
from db2 import Manufacturers, ManufacturersStorehouses, Sweets, SweetsTypes, Storehouses, ModelUser, UserToken
from datetime import timedelta, datetime
from utils import Utils
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from typing import Optional
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose.exceptions import ExpiredSignatureError, JWSError, JWTClaimsError, JWTError

app = FastAPI()

#настроика для генирации и настройки токена
SECRET_KEY = "AHDVPQURHVB[OERJVOCQEPVK-]ERKVWRBJI0FJDSNKV C[OIQERAFJC]"
# Агоритм хэширования
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#Объект для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#Модель для токена
class TokenData(BaseModel):
    username:str = None

class Token(BaseModel):
    access_token:str
    token_type:str

#Функция для гинерации токена
def create_access_token(data:dict,
                        expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes= 15)
        to_encode.update({"exp":expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

#Функция для проверки паролей
def verify_password(plain_password, heshed_password):
    return pwd_context.verify(plain_password, heshed_password)

#Функция для хэширования паролей
def get_password_hash(password):
    return pwd_context.hash(password)

#Функция для аунтификации пользователя
async def authenticate_user(username: str, password: str, users:str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user.id

#Функция для получения текущего пользователя
async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="login"))):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        token_data = TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user = get_user(username=token_data.username)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user.id
        
# Маршрут для получения токена 
@app.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_id = await authenticate_user(form_data.username, form_data.password)
    if not user_id:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/{user_id}")
async def read_user(user_id: int, current_user: int = Depends(get_current_user)):
    if user_id != current_user:
        raise HTTPException(status_code=401, detail="You don't have access to this resource")
    return {"user_id": user_id}


security = HTTPBearer()
con = DBconnect()
utils = Utils()

@app.post('/api/registrashen')
def registrashen(login: str = Body(embed=True, min_length=2, max_length=30),
                password: str =Body(embed=True, min_length=2, max_length=30),
                phone: str =Body(embed=True, regex="7\d{10}$", default = None)
                ):
    password = get_password_hash(password)
    res, error, user_id = con.isnsert(ModelUser(name=login, password=password, phone=phone))
    res = {'name': login, 'password':password}
    if res and len(error) == 0 and user_id:
        token = create_access_token(res)
        res, error, user_id = con.isnsert(UserToken(user_id = user_id, user_token= token))
        return token


@app.get('/api/all/{model}')
def all(model, user_agent:str = Header(), token: HTTPAuthorizationCredentials = Depends(security)):
    if not token:
        raise HTTPException(status_code=401, detail='Нет доступа')
    if token.credentials != "123":
        raise HTTPException(status_code=401,  detail='Нет доступа')
    print(token)
    # print(user_agent)
    match model:
        case "sweets":
            return con.select_all(Sweets)
            # return JSONResponse(sel)
        case "manufacturers":
            return con.select_all(Manufacturers)
        case "storehouses":
            return con.select_all(Storehouses)
        case "manufacturers_storehouses":
            return con.select_all(ManufacturersStorehouses)
        case "sweets_types":
            return con.select_all(SweetsTypes)
        case _:
            return False


@app.get('/api/one_select/{model}/{id}')
def one_select(model, id: int):
    match model, id:
        case "sweets", id:
            return con.select(Sweets, id)
        case "manufacturers", id:
            return con.select(Manufacturers, id)
        case "storehouses", id:
            return con.select(Storehouses, id)
        case "manufacturers_storehouses", id:
            return con.select(ManufacturersStorehouses, id)
        case "sweets_types", id:
            return con.select(SweetsTypes, id)
        case _:
            return False
        


@app.post('/api/add_sweets')
def add_sweets(name: str = Body(embed=True, min_length=2, max_length= 50),
            cost: str = Body(embed=True, min_length=1, max_length= 10),
            weight:str = Body(embed=True, min_length=1, max_length= 10),
            manufacturer_id: int = Body(embed=True, ge=1),
            production_date:str = Body(embed=True),
            expiration_date:str = Body(embed=True),
            with_sugar:bool =Body(embed=True),
            requires_freezing:bool =Body(embed=True),
            sweets_types_id: int =Body(embed=True, ge=1),
            ):

    production_date, expiration_date = utils.convert_today(production_date), utils.convert_today(expiration_date)
    if production_date != False and expiration_date  !=False:
        res, error, user_id = con.isnsert(Sweets(name = name, cost=cost, weight=weight, manufacturer_id=manufacturer_id, production_date=production_date, expiration_date=expiration_date, with_sugar=with_sugar, requires_freezing=requires_freezing, sweets_types_id=sweets_types_id))
        return {'result': res, 'error': error}
    return {'result': '', 'error': 'Date is invalide'}

@app.post('/api/update_sweets/')
def update_sweets(id: int = Body(embed=True, ge = 1),
                name: str = Body(embed=True, min_length=2, max_length= 50),
                cost: str = Body(embed=True, min_length=1, max_length= 10),
                weight:str = Body(embed=True, min_length=1, max_length= 10),
                manufacturer_id: int = Body(embed=True, ge=1),
                production_date:str = Body(embed=True),
                expiration_date:str = Body(embed=True),
                with_sugar:bool =Body(embed=True),
                requires_freezing:bool =Body(embed=True),
                sweets_types_id: int =Body(embed=True, ge=1)):
    production_date, expiration_date = utils.convert_today(production_date), utils.convert_today(expiration_date)
    if production_date != False and expiration_date  !=False:
        value = {"id": id, "name":name, "cost": cost, "weight":weight, "manufacturer_id":manufacturer_id, "production_date":production_date, "expiration_date":expiration_date, "with_sugar":with_sugar, "requires_freezing":requires_freezing, "sweets_types_id":sweets_types_id}
        res, error = con.update_field(model=Sweets, value=value)
        return {'result': res, 'error': error}
    return {'result': '', 'error': "No date"}


@app.post('/api/delet_sweets/')
def del_sweets(id: int = Body(embed=True, ge = 1)):
    res, error = con.dlt(model=Sweets, id= id)
    return {'result': res, 'error': error}

@app.post('/api/add_man/')
def add_man(name: str =Body(embed=True, min_length=2, max_length=30),
            phone: str =Body(embed=True, regex="7\d{10}$"),
            adress: str =Body(embed=True, min_length=2, max_length=999),
            city: str =Body(embed=True, min_length=2, max_length=50),
            country: str =Body(embed=True, min_length=2, max_length=50)):
    res, error, user_id= con.isnsert(Manufacturers(name=name, phone=phone, adress=adress, city=city, country=country))
    return {'result':res, 'error': error}

@app.post('/api/delet_man')
def delet_man(id: int =Body(embed=True, ge=1)):
    res, error = con.dlt(Manufacturers, id)
    return {'result': res, 'error': error}

@app.post('/api/upd_man')
def upd_man(id: int =Body(embed=True, ge=1),
            name: str =Body(embed=True, min_length=2, max_length=30),
            phone: str =Body(embed=True, regex="7\d{10}$"),
            adress: str =Body(embed=True, min_length=2, max_length=999),
            city: str =Body(embed=True, min_length=2, max_length=50),
            country: str =Body(embed=True, min_length=2, max_length=50)):
    value = {'id': id, 'name':name, 'phone': phone, 'adress': adress, 'city':city, 'country':country}
    res, error = con.update_field(Manufacturers, value)
    return {'result': res, 'error': error}

@app.post('/api/add_store/')
def add_store(name: str =Body(embed=True, min_length=2, max_length=30),
            adress: str =Body(embed=True, min_length=2, max_length=999),
            city: str =Body(embed=True, min_length=2, max_length=50),
            country: str =Body(embed=True, min_length=2, max_length=50)):
    res, error, user_id = con.isnsert(Storehouses(name=name, adress=adress, city=city, country=country))
    return {'result':res, 'error': error}

@app.post('/api/delet_store')
def delet_store(id: int = Body(embed=True, ge=1)):
    res, error = con.dlt(Storehouses, id)
    return {'result': res, 'error': error}

@app.post('/api/upd_store')
def upd_store(id: int =Body(embed=True, ge=1),
            name: str =Body(embed=True, min_length=2, max_length=30),
            adress: str =Body(embed=True, min_length=2, max_length=999),
            city: str =Body(embed=True, min_length=2, max_length=50),
            country: str =Body(embed=True, min_length=2, max_length=50)):
    value = {'id': id, 'name':name,'adress': adress, 'city':city, 'country':country}
    res, error = con.update_field(Storehouses, value)
    return {'result': res, 'error': error}

@app.post('/api/add_man_store/')
def add_man_store(storehouses_id: int =Body(embed=True, ge=1),
                manufacturers_id: int =Body(embed=True, ge=1)):
    res, error, user_id = con.isnsert(ManufacturersStorehouses(storehouses_id=storehouses_id, manufacturers_id=manufacturers_id))
    return {'result':res, 'error': error}

@app.post('/api/delet_man_store')
def delet_man_store(id: int = Body(embed=True, ge=1)):
    res, error = con.dlt(ManufacturersStorehouses, id)
    return {'result': res, 'error': error}

@app.post('/api/upd_man_store')
def upd_man_store(id: int =Body(embed=True, ge=1),
                storehouses_id: int =Body(embed=True, ge=1),
                manufacturers_id: int =Body(embed=True, ge=1)):
    value = {'id':id, 'storehouses_id': storehouses_id, 'manufacturers_id': manufacturers_id}
    res, error = con.update_field(ManufacturersStorehouses, value)
    return {'result':res, 'error': error}

@app.post('/api/add_sweets_type')
def add_sweets_type(name: str = Body(embed=True, min_length=2, max_length=50)):
    res, error, user_id = con.isnsert(SweetsTypes(name=name))
    return {'result': res, 'error': error}

@app.post('/api/delet_sweets_type')
def delet_sweets_type(id: int = Body(embed=True, ge=1)):
    res, error = con.dlt(SweetsTypes, id)
    return {'result': res, 'error': error}

@app.post('/api/upd_sweets_type')
def upd_sweets_type(id: int = Body(embed=True, ge=1),
                    name: str = Body(embed=True, min_length=2, max_length=50)):
    value = {'id':id, 'name':name}
    res, error = con.update_field(SweetsTypes, value)
    return {'result': res, 'error':error}


# class Person(BaseModel):
#     name: str
#     age: int


# class Car(BaseModel):
#     mark: str
#     model: str
#     age: int
#     volume: float  #обьем

# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#         self.id = str(uuid.uuid4())

# people = [Person("Tom", 38), Person("Bob", 42), Person("Sam", 28)]

# def take_people(id):
#     for i in people:
#         if i.id == id:
#             return i
#         return None
        
        

# @app.get("/")
# async def main():
#     return FileResponse("public/index.html")

# @app.get("/api/users")
# def get_people():
#     return people

# @app.get("/api/users/{id}")
# def get_person(id):
#     # получаем пользователя по id
#     person = take_people(id)
#     print(person)
#     # если не найден, отправляем статусный код и сообщение об ошибке
#     if person==None:  
#         return JSONResponse(
#                 status_code=status.HTTP_404_NOT_FOUND, 
#                 content={ "message": "Пользователь не найден" }
#         )
#     #если пользователь найден, отправляем его
#     return person

# @app.post("/api/users")
# def create_person(data  = Body()):
#     person = Person(data["name"], data["age"])
#     # добавляем объект в список people
#     people.append(person)
#     return person

# @app.put("/api/users")
# def edit_person(data  = Body()):

#     # получаем пользователя по id
#     person = take_people(data["id"])
#     # если не найден, отправляем статусный код и сообщение об ошибке
#     if person == None: 
#         return JSONResponse(
#                 status_code=status.HTTP_404_NOT_FOUND, 
#                 content={ "message": "Пользователь не найден" }
#         )
#     # если пользователь найден, изменяем его данные и отправляем обратно клиенту
#     person.age = data["age"]
#     person.name = data["name"]
#     return person

# @app.delete("/api/users/{id}")
# def delete_person(id):
#     # получаем пользователя по id
#     person = take_people(id)

#     # если не найден, отправляем статусный код и сообщение об ошибке
#     if person == None:
#         return JSONResponse(
#                 status_code=status.HTTP_404_NOT_FOUND, 
#                 content={ "message": "Пользователь не найден" }
#         )

#     # если пользователь найден, удаляем его
#     people.remove(person)
#     return person


# @app.get("/test")
# def root(user_agent: str = Header()):
#     return {"User-Agent": user_agent}

# @app.get("/data")
# def root(response: Response):
#     now = datetime.now()    # получаем текущую дату и время
#     response.set_cookie(key="last_visit", value=now)
#     return  {"message": "куки установлены"}

# @app.get("/data2")
# def root(last_visit = Cookie()):
#     return  {"last visit": last_visit}

# @app.get('/main')
# def main2():
#     return FileResponse('public/main.html')

# @app.post("/postdata")
# def postdata(username = Form(default="Undefined"),
#             userage: int = Form(ge=18, lt=100)):
#     return {"username": username, "userage": userage}

# @app.get("/post2")
# def main3():
#     return FileResponse("public/postdata.html")

# @app.post("/postdata2")
# def postdata2(username: str = Form(),
#             languages: list= Form()):
#     return {"username": username, "languagers": languages}


# @app.get('/')
# def read_root():
#     data = {"message": "Hello Metanit"}
#     json_data = jsonable_encoder(data)
#     return JSONResponse(content = json_data)


# @app.get('/main')
# def root():
#     data = {"message": "Hello Metanit"}
#     json_data = jsonable_encoder(data)
#     return Response(content =json_data , media_type = "application/json")

# @app.get('/about')
# def about():
#     data = "hello world 2"
#     return PlainTextResponse(content = data)


# @app.get('/root')
# def root_task():
#     data = '<h2>Hellow word3</h2>'
#     return HTMLResponse(content = data)

# @app.get('/file')
# def root_file():
#     return FileResponse("public/Python - 08.pdf", filename = "Python - 08.pdf", media_type = "application/pdf")

# @app.get("/users/{phone}")
# def users(phone: str = Path(regex = '^375(25|29|33|44)\d{7}$')):
#     return {"phone": phone}


# @app.get("/users2/{name}/{age}")
# def users2(name, age):
#     return {"user_name": name, "user_age": age}

# @app.get("/users3/{id}")
# def users3(id: int):
#     return {"user_id": id}

# @app.get("/users4/{name}")
# def users4(name:str  = Path(min_length=3, max_length=20)):
#     return {"name": name}

# @app.get("/users5")
# def get_model(name, age):
#     return {"user_name": name, "user_age": age}

# @app.get("/users6")
# def users(people: list[str]  = Query()):
#     return {"people": people}

# @app.get("/notfound")
# def notfound():
#     return JSONResponse(content={"message": "Resource Not Found"}, status_code=417)

# @app.get("/old")
# def old():
#     return RedirectResponse("/new")

# @app.get("/new")
# def new():
#     return PlainTextResponse("Новая страница")

# @app.get("/")
# def root():
#     return FileResponse("public/index.html")

# @app.post("/hello")
#def hello(name = Body(embed=True)):
# def hello(person: Person):
#     return {"message": f"Привет, {person.name}, твой возраст - {person.age}"}

# @app.get("/")
# def root2():
#     return FileResponse("public/about.html")

# @app.post("/task")
# def task(car: Car):
#     return {"message": f"Автомобиль, {car.mark}, модель - {car.model}, год выпуска - {car.age}, обьем - {car.volume},"}