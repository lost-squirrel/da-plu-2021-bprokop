from fastapi import FastAPI
from app.routers import deploy, art, fast, table
from .views import router as northwind_api_router


app = FastAPI()

app.include_router(deploy.router)
app.include_router(art.router)
app.include_router(fast.router)
app.include_router(table.router)
app.include_router(northwind_api_router, tags=["northwind"])


@app.on_event('startup')
async def startup():
    await table.startup()


@app.on_event("shutdown")
async def shutdown():
    await table.shutdown()
