from fastapi import FastAPI, Request, HTTPException, Query, Response
from typing import Optional
import hashlib
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
def method_put(request: Request):
    return {"method": request.method}


@app.options("/method")
def method_options(request: Request):
    return {"method": request.method}


@app.delete("/method")
def method_delete(request: Request):
    return {"method": request.method}


@app.post("/method", status_code=201)
def method_post(request: Request):
    return {"method": request.method}


@app.get("/auth")
def auth_view(password: Optional[str] = Query(None), password_hash: Optional[str] = Query(None)):
    if password and password_hash and password.strip() and password_hash.strip():
        calculated_hash = hashlib.sha512(password.encode()).hexdigest()
        if calculated_hash == password_hash:
            return Response(status_code=204)
    return Response(status_code=401)
