USE HOMEWORK;
CREATE TABLE De46pot (
    DepotID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Location VARCHAR(100) NOT NULL,
    Capacity DECIMAL(10, 2) NOT NULL CHECK (Capacity > 0)
);

INSERT INTO De46pot (DepotID, Name, Location, Capacity) VALUES
('D01', '魏公村油库', '魏公村', 20000),
('D02', '东直门油库', '东直门', 15000),
('D03', '青龙湖油库', '青龙湖', 10000);

INSERT INTO De46pot (DepotID, Name, Location, Capacity) VALUES
('D04', '西城区油库', '西城区', 18000),
('D05', '海淀区油库', '海淀区', 16000);

