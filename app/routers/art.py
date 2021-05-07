import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["art"])


dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../decorators/decorators.py')
with open(filename, 'r') as decorators:
    data = decorators.read()

data = "<html><body><pre>" + data + "</pre></body></html>"


@router.get("/art")
def art_view():
    return HTMLResponse(data)
