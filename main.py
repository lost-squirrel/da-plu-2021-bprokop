from fastapi import FastAPI, Request

from pydantic import BaseModel

app = FastAPI()
app.counter = 0


class HelloResp(BaseModel):
    msg: str


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/hello/{name}")
def hello_name_view(name: str):
    return f"Hello {name}"


@app.get("/counter")
def counter():
    app.counter += 1
    return app.counter


@app.get("/method")
def method_view(request: Request):
    return {"method": request.method}


@app.put("/method")
def method_view(request: Request):
    return {"method": request.method}


@app.options("/method")
def method_view(request: Request):
    return {"method": request.method}


@app.delete("/method")
def method_view(request: Request):
    return {"method": request.method}


@app.post("/method", status_code=201)
def method_view(request: Request):
    return {"method": request.method}
