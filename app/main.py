import os
import sqlite3
from typing import Optional
from fastapi import FastAPI, HTTPException
from starlette.requests import HTTPConnection
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
    COALESCE(Address, '') || ' ' || COALESCE(PostalCode, '') || ' ' || COALESCE(City, '') || ' ' || COALESCE(Country, '') as full_address 
    FROM Customers 
    ORDER BY UPPER(CustomerID)
    """).fetchall()
    return {"customers": customers}

@app.get("/products/{id}")
async def product_view(id: int):
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    product = cursor.execute("""
    SELECT ProductID as id, ProductName as name 
    FROM Products 
    WHERE id=:id    
    """, {"id": id}).fetchone()
    if not product:
        raise HTTPException(404)
    return product

@app.get("/employees")
async def employees_view(order: Optional[str] = None, limit: int = -1, offset: int = 0):
    if order not in {'first_name', 'last_name', 'city', None}:
        raise HTTPException(400)
    order = order or 'id'
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    employees = cursor.execute("""
    SELECT EmployeeID as id, LastName as last_name, FirstName as first_name, City as city
    FROM Employees
    ORDER BY {} LIMIT {} OFFSET {}
    """.format(order, limit, offset)).fetchall()
    return {"employees": employees}



