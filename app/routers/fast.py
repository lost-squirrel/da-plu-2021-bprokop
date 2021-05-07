from collections import deque
from typing import Optional
from datetime import date
import os
import secrets
from fastapi import APIRouter, Request, Response, Depends, Cookie, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse, HTMLResponse, RedirectResponse

router = APIRouter(tags=["fast"])
directory = os.path.dirname(__file__)
security = HTTPBasic()
template_path = os.path.join(directory, '../templates')
templates = Jinja2Templates(directory=template_path)
router.secret_key = "v3r1 s1kr3t k3y"
router.sessions = deque([], maxlen=3)
router.tokens = deque([], maxlen=3)


@router.get("/hello")
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


@router.post("/login_session", status_code=201)
def create_session_cookie(response: Response, user=Depends(verify_credentials)):
    session_token = secrets.token_urlsafe()
    router.sessions.appendleft(session_token)
    response.set_cookie(key="session_token", value=session_token)
    return {"user": user["name"]}


@router.post("/login_token", status_code=201)
def get_session_token(response: Response, user=Depends(verify_credentials)):
    token = secrets.token_urlsafe()
    router.tokens.appendleft(token)
    return {"token": token}


def generate_welcome_response(format):
    if format == "json":
        return {"message": "Welcome!"}
    elif format == "html":
        html_content = """
        <html>
            <head>
                <title></title>
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
            </body>app
            """
        return HTMLResponse(content=html_content, status_code=200)
    else:
        return PlainTextResponse(content="Logged out!", status_code=200)


@router.get("/welcome_session")
def welcome_session_view(session_token: Optional[str] = Cookie(None), format: Optional[str] = None):
    if session_token in router.sessions:
        return generate_welcome_response(format)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized session")


@router.get("/welcome_token")
def welcome_token_view(token: Optional[str] = None, format: Optional[str] = None):
    if token in router.tokens:
        return generate_welcome_response(format)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized token")


@router.delete("/logout_session")
def delete_session(request: Request, session_token: Optional[str] = Cookie(None), format: Optional[str] = ""):
    if session_token in router.sessions:
        router.sessions.remove(session_token)
        url = f"/logged_out?format={format}"
        return RedirectResponse(url, status_code=status.HTTP_302_FOUND)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized session")


@router.delete("/logout_token")
def delete_token(request: Request, token: Optional[str] = None, format: Optional[str] = ""):
    if token in router.tokens:
        router.tokens.remove(token)
        url = f"/logged_out?format={format}"
        return RedirectResponse(url, status_code=status.HTTP_302_FOUND)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized session")


@router.get("/logged_out")
def logged_out_view(format: Optional[str] = None):
    return generate_logout_response(format)
