USE HOMEWORK;
CREATE TABLE Oi46lInventory (
    OilTypeID VARCHAR(20),
    Inventory DECIMAL(10, 2) NOT NULL CHECK (Inventory >= 0),
    DepotID VARCHAR(20),
    PRIMARY KEY(OilTypeID, DepotID),
    FOREIGN KEY(OilTypeID) REFERENCES Oi46lType(OilTypeID),
    FOREIGN KEY(DepotID) REFERENCES De46pot(DepotID)
);

INSERT INTO Oi46lInventory (OilTypeID, Inventory, DepotID) VALUES
('OT01', 5000, 'D03'),
('OT02', 6000, 'D01'),
('OT03', 4000, 'D01'),
('OT04', 3000, 'D02'),
('OT05', 7000, 'D01');

INSERT INTO Oi46lInventory (OilTypeID, Inventory, DepotID) VALUES
('OT01', 2000, 'D04'),
('OT02', 3000, 'D05');
