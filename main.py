import secrets
from fastapi import FastAPI, Request, HTTPException, Query, Response, Depends, Cookie, status
from fastapi.responses import PlainTextResponse, HTMLResponse, RedirectResponse
from typing import Optional
from hashlib import sha256, sha512
from pydantic import BaseModel
from datetime import date, timedelta
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()
templates = Jinja2Templates(directory="templates")
app.secret_key = "veri sikret key"
app.session = None
app.token = None
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


@app.get("/hello")
def plain_hello_view(request: Request):
    return templates.TemplateResponse("hello.html.j2", {"date": date.today(), "request": request})


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(
        credentials.password, "NotSoSecurePa$$")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"name": correct_username, "password": correct_password}


@app.post("/login_session", status_code=201)
def create_session_cookie(response: Response, user=Depends(verify_credentials)):
    session_token = "token1234"
    app.session = session_token
    response.set_cookie(key="session_token", value=session_token)
    return {"user": user["name"]}


@app.post("/login_token", status_code=201)
def get_session_token(response: Response, user=Depends(verify_credentials)):
    token = "token1234"
    app.token = token
    return {"token": token}


def generate_welcome_response(format):
    if format == "json":
        return {"message": "Welcome!"}
    elif format == "html":
        html_content = """
        <html>
            <head>
                <title</title>
            </head>
            <body>
                <h1>Welcome!</h1>
            </body>
        </html>
            """
        return HTMLResponse(content=html_content, status_code=200)
    else:
        return PlainTextResponse(content="Welcome!", status_code=200)


def generate_logout_response(format):
    if format == "json":
        return {"message": "Logged out!"}
    elif format == "html":
        html_content = """
        <html>
            <head>
                <title</title>
            </head>
            <body>
                <h1>Logged out!</h1>
            </body>
        </html>
            """
        return HTMLResponse(content=html_content, status_code=200)
    else:
        return PlainTextResponse(content="Logged out!", status_code=200)


@app.get("/welcome_session")
def welcome_session_view(session_token: Optional[str] = Cookie(None), format: Optional[str] = None):
    if app.session and session_token and secrets.compare_digest(app.session, session_token):
        return generate_welcome_response(format)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized session")


@app.get("/welcome_token")
def welcome_token_view(token: Optional[str] = None, format: Optional[str] = None):
    if app.token and token and secrets.compare_digest(app.token, token):
        return generate_welcome_response(format)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized token")


@app.delete("/logout_session")
def delete_session(request: Request, session_token: Optional[str] = Cookie(None), format: Optional[str] = ""):
    if app.session and session_token and secrets.compare_digest(app.session, session_token):
        app.session = None
        url = f"/logged_out?format={format}"
        return RedirectResponse(url, 301)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized session")


@app.delete("/logout_token")
def delete_token(request: Request, token: Optional[str] = None, format: Optional[str] = ""):
    if app.token and token and secrets.compare_digest(app.token, token):
        app.token = None
        url = f"/logged_out?format={format}"
        return RedirectResponse(url, 301)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized session")


@app.delete("/logged_out")
def logged_out_view(format: Optional[str] = None):
    return generate_logout_response(format)


@app.get("/hello/{name}")
def hello_name_view(name: str):
    return f"Hello {name}"


@app.get("/counter")
def counter():
    app.counter += 1
    surname = patient_info.surname,


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


@app.get("/patient/{id}", response_model=PatientData)
def patient_view(id: int):
    if id < 1:
        return Response(status_code=400)
    if id in app.mock_db:
        return app.mock_db[id]
    return Response(status_code=404)
