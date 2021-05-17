ALTER TABLE products
ADD FOREIGN KEY ("SupplierID") REFERENCES suppliers("SupplierID");

ALTER TABLE products
ADD FOREIGN KEY ("CategoryID") REFERENCES categories("CategoryID");

ALTER TABLE orders
ADD FOREIGN KEY ("CustomerID") REFERENCES customers("CustomerID");

ALTER TABLE orders
ADD FOREIGN KEY ("EmployeeID") REFERENCES employees("EmployeeID");

ALTER TABLE orders
ADD FOREIGN KEY ("ShipVia") REFERENCES shippers("ShipperID");