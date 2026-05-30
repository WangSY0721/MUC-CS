USE HOMEWORK;
CREATE TABLE Oi46lType (
    OilTypeID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL CHECK (Price >= 0)
);

ALTER TABLE Oi46lType
MODIFY COLUMN Name ENUM('92#汽油', '93#汽油', '95#汽油', '97#汽油', '柴油') NOT NULL;

CREATE INDEX idx_OilTypeName ON Oi46lType(Name);
INSERT INTO Oi46lType (OilTypeID, Name, Price) VALUES
('OT01', '92#汽油', 6.50),
('OT02', '93#汽油', 7.00),
('OT03', '95#汽油', 7.50),
('OT04', '97#汽油', 8.00),
('OT05', '柴油', 5.50);
