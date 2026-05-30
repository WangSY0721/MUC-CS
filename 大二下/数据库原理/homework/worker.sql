USE HOMEWORK;
CREATE TABLE Wo46rker (
    WorkerID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    IDNumber CHAR(18) NOT NULL UNIQUE,
    WorkerType VARCHAR(20) NOT NULL,
    Password VARCHAR(50) NOT NULL
);

ALTER TABLE Wo46rker
MODIFY COLUMN WorkerType ENUM('销售', '财务', '前台', '经理') NOT NULL;

ALTER TABLE Wo46rker
ADD COLUMN Phone VARCHAR(20) NOT NULL;

INSERT INTO Wo46rker (WorkerID, Name, IDNumber, WorkerType, Password, Phone) VALUES
('W001', '张三', '110101199003075555', '销售', 'password1', '12345678901'),
('W002', '李四', '110101199003076666', '财务', 'password2', '12345678902'),
('W003', '王五', '110101199003077777', '前台', 'password3', '12345678903'),
('W004', '赵六', '110101199003078888', '经理', 'password4', '12345678904'),
('W005', '孙七', '110101199003079999', '销售', 'password5', '12345678905');

INSERT INTO Wo46rker (WorkerID, Name, IDNumber, WorkerType, Password, Phone) VALUES
('W006', '李丽', '110101199003071111', '销售', 'password6', '12345678906'),
('W007', '王红', '110101199003072222', '前台', 'password7', '12345678907');