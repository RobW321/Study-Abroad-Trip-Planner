CREATE TABLE expenses (
    id INT IDENTITY(1,1) PRIMARY KEY,
    trip_id INT NOT NULL,
    description NVARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    category NVARCHAR(100) NOT NULL
);