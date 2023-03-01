from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse, FileResponse
from fastapi.encoders import jsonable_encoder
import mimetypes



app =FastAPI()

@app.get('/')
def read_root():
    data = {"message": "Hello Metanit"}
    json_data = jsonable_encoder(data)
    return JSONResponse(content = json_data)


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

@app.get("/users/{id}")
def users(id):
    return {"user_id": id}

