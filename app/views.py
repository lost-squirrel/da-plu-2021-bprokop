from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db

router = APIRouter()


@router.get("/shippers/{shipper_id}", response_model=schemas.Shipper)
async def get_shipper(shipper_id: PositiveInt, db: Session = Depends(get_db)):
    db_shipper = crud.get_shipper(db, shipper_id)
    if db_shipper is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_shipper


@router.get("/shippers", response_model=List[schemas.Shipper])
async def get_shippers(db: Session = Depends(get_db)):
    return crud.get_shippers(db)


@router.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def get_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


@router.get("/suppliers", response_model=List[schemas.Supplier], response_model_exclude_none=True)
async def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)


@router.post("/suppliers", status_code=201, response_model=schemas.Supplier, response_model_exclude={"Region"})
async def create_supplier(supplier: schemas.Supplier_Create, db: Session = Depends(get_db)):
    return crud.create_supplier(db, supplier.dict())


@router.get("/suppliers/{supplier_id}/products", response_model=List[schemas.Product])
async def get_supplier_products(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db_products = crud.get_supplier_products(db, supplier_id)
    return db_products


@router.put("/suppliers/{supplier_id}", status_code=200, response_model=schemas.Supplier, response_model_exclude={"Region"})
async def update_supplier(supplier_id: PositiveInt, supplier: schemas.Supplier_Update, db: Session = Depends(get_db)):
    updated_supplier = crud.update_supplier(db, supplier_id, supplier)
    if updated_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return updated_supplier


@router.delete("/suppliers/{supplier_id}", status_code=204)
async def delete_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    if crud.get_supplier(db, supplier_id) is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return crud.delete_supplier(db, supplier_id)
