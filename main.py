from fastapi import FastAPI, Request, HTTPException, Query, Response
from typing import Optional
from hashlib import sha512
from pydantic import BaseModel
from datetime import date, timedelta

app = FastAPI()
app.counter = 0
app.patient_id = 0
app.mock_db = {}


class HelloResp(BaseModel):
    msg: str


class PatientData(BaseModel):
    id: int
    name: str
    surname: str
    register_date: date
    vaccination_date: date


class PatientInfo(BaseModel):
    name: str
    surname: str


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
        calculated_hash = sha512(password.encode()).hexdigest()
        if calculated_hash == password_hash:
            return Response(status_code=204)
    return Response(status_code=401)


@app.post("/register", status_code=201, response_model=PatientData)
def patient_register(patient_info: PatientInfo):
    app.patient_id += 1
    register_date = date.today()
    letters_in_names = sum(1 for _ in filter(
        str.isalpha, patient_info.name + patient_info.surname))
    vaccination_date = register_date + timedelta(days=letters_in_names)
    patient = PatientData(
        id=app.patient_id,
        name=patient_info.name,
        surname=patient_info.surname,
        register_date=register_date,
        vaccination_date=vaccination_date
    )
    app.mock_db[app.patient_id] = patient
    return patient
