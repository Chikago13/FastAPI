from fastapi import FastAPI, Response, Path, Query, Body
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse, FileResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
import mimetypes
from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int

app =FastAPI()

class Car(BaseModel):
    mark: str
    model: str
    age: int
    volume: float  #обьем

app = FastAPI()


# @app.get('/')
# def read_root():
#     data = {"message": "Hello Metanit"}
#     json_data = jsonable_encoder(data)
#     return JSONResponse(content = json_data)


@app.get('/main')
def root():
    data = {"message": "Hello Metanit"}
    json_data = jsonable_encoder(data)
    return Response(content =json_data , media_type = "application/json")

@app.get('/about')
def about():
    data = "hello world 2"
    return PlainTextResponse(content = data)


@app.get('/root')
def root_task():
    data = '<h2>Hellow word3</h2>'
    return HTMLResponse(content = data)

@app.get('/file')
def root_file():
    return FileResponse("public/Python - 08.pdf", filename = "Python - 08.pdf", media_type = "application/pdf")

@app.get("/users/{phone}")
def users(phone: str = Path(regex = '^375(25|29|33|44)\d{7}$')):
    return {"phone": phone}


@app.get("/users2/{name}/{age}")
def users2(name, age):
    return {"user_name": name, "user_age": age}

@app.get("/users3/{id}")
def users3(id: int):
    return {"user_id": id}

@app.get("/users4/{name}")
def users4(name:str  = Path(min_length=3, max_length=20)):
    return {"name": name}

@app.get("/users5")
def get_model(name, age):
    return {"user_name": name, "user_age": age}

@app.get("/users6")
def users(people: list[str]  = Query()):
    return {"people": people}

@app.get("/notfound")
def notfound():
    return JSONResponse(content={"message": "Resource Not Found"}, status_code=417)

@app.get("/old")
def old():
    return RedirectResponse("/new")

@app.get("/new")
def new():
    return PlainTextResponse("Новая страница")

# @app.get("/")
# def root():
#     return FileResponse("public/index.html")

@app.post("/hello")
#def hello(name = Body(embed=True)):
def hello(person: Person):
    return {"message": f"Привет, {person.name}, твой возраст - {person.age}"}

@app.get("/")
def root2():
    return FileResponse("public/about.html")

@app.post("/task")
def task(car: Car):
    return {"message": f"Автомобиль, {car.mark}, модель - {car.model}, год выпуска - {car.age}, обьем - {car.volume},"}