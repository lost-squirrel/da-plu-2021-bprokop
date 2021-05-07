from fastapi import FastAPI
from app.routers import deploy, art, fast

app = FastAPI()
app.include_router(deploy.router)
app.include_router(art.router)
app.include_router(fast.router)
