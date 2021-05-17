import os
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from typing import Optional
import sqlite3

router = APIRouter(tags=["table"])


async def startup():
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, "../db/northwind.db")
    router.db_connection = sqlite3.connect(filename)
    router.db_connection.text_factory = lambda b: b.decode(errors="ignore")
    router.cursor = router.db_connection.cursor()
    router.cursor.row_factory = sqlite3.Row


async def shutdown():
    router.db_connection.close()


class Category(BaseModel):
    name: str


@router.get("/categories")
async def categories_view():
    categories = router.cursor.execute("""
    SELECT CategoryID as id, CategoryName as name
    FROM Categories
    ORDER BY UPPER(CategoryName)""").fetchall()
    return {"categories": categories}


@router.post("/categories", status_code=201)
async def add_category(category: Category):
    cursor = router.cursor.execute("""
    INSERT INTO Categories (CategoryName) 
    VALUES (?)
    """, (category.name,))
    router.db_connection.commit()
    new_category_id = cursor.lastrowid
    category = router.cursor.execute("""
    SELECT CategoryID as id, CategoryName as name
    FROM Categories WHERE CategoryID = ?
    """, (new_category_id,)).fetchone()
    return category


@router.put("/categories/{id}", status_code=200)
async def update_category(id: int, category: Category):
    router.cursor.execute("""
    UPDATE Categories
    SET CategoryName = ?
    WHERE CategoryID = ?
    """, (category.name, id))
    router.db_connection.commit()
    category = router.cursor.execute("""
    SELECT CategoryID AS id, CategoryName AS name
    FROM Categories
    WHERE CategoryID = ?
    """, (id, )).fetchone()
    if not category:
        raise HTTPException(404)
    return category


@router.delete("/categories/{id}", status_code=200)
async def delete_category(id: int):
    cursor = router.cursor.execute("""
    DELETE FROM Categories
    WHERE CategoryID = ?
    """, (id, ))
    router.db_connection.commit()
    if not cursor.rowcount:
        raise HTTPException(404)
    return {"deleted": 1}


@router.get("/customers")
async def customers_view():
    customers = router.cursor.execute("""
    SELECT CustomerID as id, COALESCE(CompanyName, '') as name,
    COALESCE(Address, '') || ' ' || COALESCE(PostalCode, '') || ' ' || COALESCE(City, '') || ' ' || COALESCE(Country, '') as full_address
    FROM Customers
    ORDER BY UPPER(CustomerID)
    """).fetchall()
    return {"customers": customers}


@router.get("/products/{id}")
async def product_view(id: int):
    product = router.cursor.execute("""
    SELECT ProductID as id, ProductName as name
    FROM Products
    WHERE id=:id
    ORDER BY UPPER(ProductID)
    """, {"id": id}).fetchone()
    if not product:
        raise HTTPException(404)
    return product


@router.get("/employees")
async def employees_view(order: Optional[str] = None, limit: int = -1, offset: int = 0):
    if order not in {'first_name', 'last_name', 'city', None}:
        raise HTTPException(400)
    order = order or 'id'
    employees = router.cursor.execute("""
    SELECT EmployeeID as id, LastName as last_name, FirstName as first_name, City as city
    FROM Employees
    ORDER BY {} LIMIT {} OFFSET {}
    """.format(order, limit, offset)).fetchall()
    return {"employees": employees}


@router.get("/products_extended")
async def products_extended_view():
    products_extended = router.cursor.execute("""
    SELECT Products.ProductID as id, Products.ProductName as name, Categories.CategoryName as category, Suppliers.CompanyName as supplier
    FROM Products
    JOIN Categories ON Products.CategoryID = Categories.CategoryID
    JOIN Suppliers ON Products.SupplierID = Suppliers.SupplierID
    """).fetchall()
    return {"products_extended": products_extended}


@router.get("/products/{id}/orders")
async def products_orders_view(id: int):
    orders = router.cursor.execute("""
    SELECT Orders.OrderID as id, Customers.CompanyName as customer, od.Quantity as quantity, round( od.Quantity * od.UnitPrice * (1-od.Discount) , 2) as total_price
    FROM Orders
    JOIN Customers ON Orders.CustomerID = Customers.CustomerID
    JOIN 'Order Details' od on Orders.OrderID = od.OrderID
    AND od.ProductID=:id
    """, {"id": id}).fetchall()
    if not orders:
        raise HTTPException(404)
    return {"orders": orders}
