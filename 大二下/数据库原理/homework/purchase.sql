USE HOMEWORK;
CREATE TABLE Pu46rchase (
    PurchaseTime TIMESTAMP NOT NULL,
    OilTypeID VARCHAR(20),
    DepotID VARCHAR(20),
    WorkerID VARCHAR(20),
    Quantity DECIMAL(10, 2) NOT NULL CHECK (Quantity > 0),
    UnitPrice DECIMAL(10, 2) NOT NULL CHECK (UnitPrice >= 0),
    PRIMARY KEY(PurchaseTime, OilTypeID, DepotID, WorkerID),
    FOREIGN KEY(OilTypeID) REFERENCES Oi46lType(OilTypeID),
    FOREIGN KEY(DepotID) REFERENCES De46pot(DepotID),
    FOREIGN KEY(WorkerID) REFERENCES Wo46rker(WorkerID)
);

INSERT INTO Pu46rchase (PurchaseTime, OilTypeID, DepotID, WorkerID, Quantity, UnitPrice) VALUES
('2024-04-08 09:00:00', 'OT01', 'D03', 'W001', 1000, 6.30),
('2024-04-08 10:00:00', 'OT02', 'D01', 'W002', 500, 6.80);

INSERT INTO Pu46rchase (PurchaseTime, OilTypeID, DepotID, WorkerID, Quantity, UnitPrice) VALUES
('2024-03-03 00:00:00', 'OT01', 'D01', 'W006', 1000, 6.30);
