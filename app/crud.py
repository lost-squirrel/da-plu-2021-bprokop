from sqlalchemy import asc, desc, update
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import delete

from . import models
from .schemas import Supplier_Create, Supplier_Update


def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(
            models.Shipper.ShipperID == shipper_id).first()
    )


def get_suppliers(db: Session):
    return db.query(models.Supplier.SupplierID, models.Supplier.CompanyName).order_by(asc(models.Supplier.SupplierID)).all()


def get_supplier(db: Session, supplier_id: int):
    return (
        db.query(models.Supplier).filter(
            models.Supplier.SupplierID == supplier_id).first()
    )


def get_supplier_products(db: Session, supplier_id: int):
    return (
        db.query(models.Product.ProductID, models.Product.ProductName, models.Category, models.Product.Discontinued).join(models.Category).filter(
            models.Product.SupplierID == supplier_id).order_by(desc(models.Product.ProductID)) .all()
    )


def create_supplier(db: Session, supplier_in: Supplier_Create):
    newSupplier = models.Supplier(**supplier_in)
    db.add(newSupplier)
    db.commit()
    return newSupplier


def update_supplier(db: Session, supplier_id: int, supplier: Supplier_Update):
    values = {k: v for k, v in supplier.dict().items() if v is not None}
    if values:
        stmt = update(models.Supplier).where(
            models.Supplier.SupplierID == supplier_id).values(values).execution_options(synchronize_session="fetch")
        db.execute(stmt)
        db.commit()
    return get_supplier(db, supplier_id)


def delete_supplier(db: Session, supplier_id: int):
    stmt = delete(models.Supplier).where(models.Supplier.SupplierID == supplier_id).execution_options(
        synchronize_session="fetch")
    db.execute(stmt)
    db.commit()
    return
