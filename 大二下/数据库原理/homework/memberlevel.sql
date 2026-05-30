USE HOMEWORK;
CREATE TABLE Me46mberLevel (
    LevelID VARCHAR(20) PRIMARY KEY,
    LevelName VARCHAR(50) NOT NULL,
    Discount DECIMAL(3, 2) NOT NULL CHECK (Discount >= 0 AND Discount <= 1),
    MinSpending DECIMAL(10, 2) NOT NULL CHECK (MinSpending >= 0)
);

ALTER TABLE Me46mberLevel
ADD CONSTRAINT CHK_LevelName CHECK (LevelName IN ('金卡', '银卡', '铜卡', '普通会员'));

INSERT INTO Me46mberLevel (LevelID, LevelName, Discount, MinSpending) VALUES
('LV01', '普通会员', 0.00, 0),
('LV02', '铜卡', 0.05, 1000),
('LV03', '银卡', 0.10, 5000),
('LV04', '金卡', 0.15, 10000);
