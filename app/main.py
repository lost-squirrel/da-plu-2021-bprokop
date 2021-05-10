import os
import sqlite3
from fastapi import FastAPI
from app.routers import deploy, art, fast


app = FastAPI()

app.include_router(deploy.router)
app.include_router(art.router)
app.include_router(fast.router)

@app.on_event('startup')
async def startup():
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, "db/northwind.db")
    app.db_connection = sqlite3.connect(filename)
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")

@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

@app.get("/categories")
async def categories_view():
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    categories = cursor.execute("""
    SELECT CategoryID as id, CategoryName as name
    FROM Categories 
    ORDER BY UPPER(CategoryName)""").fetchall()
    return {"categories": categories}

@app.get("/customers")
async def customers_view():
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    customers = cursor.execute("""
    SELECT CustomerID as id, COALESCE(CompanyName, '') as name,
    COALESCE(Address, '') || ' ' || COALESCE(PostalCode, '') || ' ' || COALESCE(City, '') || ' ' || COALESCE(Country, '') as full_adress 
    FROM Customers 
    ORDER BY UPPER(CustomerID)
    """).fetchall()
    return {"customers": customers}

