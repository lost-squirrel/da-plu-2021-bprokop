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


@app.get("/products_extended")
async def products_extended_view():
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    products_extended = cursor.execute("""
    SELECT Products.ProductID as id, Products.ProductName as name, Categories.CategoryName as category, Suppliers.CompanyName as supplier
    FROM Products
    JOIN Categories ON Products.CategoryID = Categories.CategoryID
    JOIN Suppliers ON Products.SupplierID = Suppliers.SupplierID
    """).fetchall()
    return {"products_extended": products_extended}


@app.get("/products/{id}/orders")
async def products_orders_view(id: int):
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    orders = cursor.execute("""
    SELECT Orders.OrderID as id, Customers.CompanyName as customer, od.Quantity as quantity, round( od.Quantity * od.UnitPrice * (1-od.Discount) , 2) as total_price
    FROM Orders
    JOIN Customers ON Orders.CustomerID = Customers.CustomerID
    JOIN 'Order Details' od on Orders.OrderID = od.OrderID
    AND od.ProductID=:id
    """, {"id": id}).fetchall()
    if not orders:
        raise HTTPException(404)
    return {"orders": orders}
