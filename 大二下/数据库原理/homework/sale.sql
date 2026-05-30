USE HOMEWORK;
CREATE TABLE Sa46le (
    SaleTime TIMESTAMP NOT NULL,
    OilTypeID VARCHAR(20),
    DepotID VARCHAR(20),
    Quantity DECIMAL(10, 2) NOT NULL CHECK (Quantity > 0),
    UnitPrice DECIMAL(10, 2) NOT NULL CHECK (UnitPrice >= 0),
    WorkerID VARCHAR(20),
    Customer VARCHAR(50),
    Discount DECIMAL(3, 2) NOT NULL CHECK (Discount >= 0 AND Discount <= 1),
    PRIMARY KEY(SaleTime, OilTypeID, DepotID, WorkerID),
    FOREIGN KEY(OilTypeID) REFERENCES Oi46lType(OilTypeID),
    FOREIGN KEY(DepotID) REFERENCES De46pot(DepotID),
    FOREIGN KEY(Customer) REFERENCES Me46mber(MemberID),
    FOREIGN KEY(WorkerID) REFERENCES Wo46rker(WorkerID)
);

INSERT INTO Sa46le (SaleTime, OilTypeID, DepotID, Quantity, UnitPrice, WorkerID, Customer, Discount) VALUES
('2024-03-10 10:00:00', 'OT01', 'D01', 200, 6.70, 'W003', 'M001', 0.1),
('2024-02-28 11:00:00', 'OT03', 'D01', 300, 7.60, 'W004', 'M002', 0.05),
('2024-04-12 09:00:00', 'OT02', 'D01', 150, 7.10, 'W005', 'M003', 0.15);

INSERT INTO Sa46le (SaleTime, OilTypeID, DepotID, Quantity, UnitPrice, WorkerID, Customer, Discount) VALUES
('2024-03-03 00:00:00', 'OT01', 'D01', 30, 6.50, 'W007', 'M007', 0.15);


