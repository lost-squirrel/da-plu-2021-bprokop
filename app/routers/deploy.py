from hashlib import sha512
from datetime import date, datetime, timedelta
from typing import Optional
from fastapi import Query, HTTPException, Request, Response, status, APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["deploy"])

router.patient_id = 0
router.mock_db = {}


class PatientData(BaseModel):
    id: int
    name: str
    surname: str
    register_date: date
    vaccination_date: date


class PatientInfo(BaseModel):
    name: str
    surname: str


@router.get("/")
def root():
    return {"message": "Hello world!"}


@router.api_route(path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"], status_code=200)
def method_view(request: Request, response: Response):
    if request.method == "POST":
        response.status_code = status.HTTP_201_CREATED
    return {"method": request.method}


@router.get("/auth")
def auth_view(password: Optional[str] = Query(None), password_hash: Optional[str] = Query(None)):
    if password and password_hash and password.strip() and password_hash.strip():
        calculated_hash = sha512(password.encode()).hexdigest()
        if calculated_hash == password_hash:
            return Response(status_code=204)
    raise HTTPException(status_code=401)


@router.post("/register", status_code=201, response_model=PatientData)
def patient_register(patient_info: PatientInfo):
    router.patient_id += 1
    register_date = date.today()
    letters_in_names = sum(1 for _ in filter(
        str.isalpha, patient_info.name + patient_info.surname))
    vaccination_date = register_date + timedelta(days=letters_in_names)
    patient = PatientData(
        id=router.patient_id,
        name=patient_info.name,
        surname=patient_info.surname,
        register_date=register_date,
        vaccination_date=vaccination_date
    )
    router.mock_db[router.patient_id] = patient
    return patient


@router.get("/patient/{id}", response_model=PatientData)
def patient_view(id: int):
    if id < 1:
        raise HTTPException(status_code=400)
    if id in router.mock_db:
        return router.mock_db[id]
        raise HTTPException(status_code=404)
