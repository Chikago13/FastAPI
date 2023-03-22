from fastapi import FastAPI, Response, Path, Query, Body, status, Header, Cookie, Form
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse, FileResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
import mimetypes, uuid
from pydantic import BaseModel
from datetime import datetime
from datebase import DBconnect
from db2 import Manufacturers, ManufacturersStorehouses, Sweets, SweetsTypes, Storehouses
import datetime
from utils import Utils

app = FastAPI()
con = DBconnect()
utils = Utils()

@app.get('/api/all/{model}')
def all(model):
    match model:
        case "sweets":
            return con.select_all(Sweets)
            # return JSONResponse(sel)
        case "manufacturers":
            return con.select_all(Manufacturers)
        case "storehouses":
            return con.select_all(Storehouses)
        case _:
            return False


@app.get('/api/one_select/{model}/{id}')
def one_select(model, id: int):
    match model:
        case "sweets":
            return con.select(Sweets, id)
        case "manufacturers":
            return con.select(Manufacturers, id)
        case "storehouses":
            return con.select(Storehouses, id)
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
        res, error = con.isnsert(Sweets(name = name, cost=cost, weight=weight, manufacturer_id=manufacturer_id, production_date=production_date, expiration_date=expiration_date, with_sugar=with_sugar, requires_freezing=requires_freezing, sweets_types_id=sweets_types_id))
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