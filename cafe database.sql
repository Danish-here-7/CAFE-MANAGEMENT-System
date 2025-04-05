-- Create Database
CREATE DATABASE  danishdb;
USE danishdb;

-- Menu Table
CREATE TABLE IF NOT EXISTS Menu (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL,
    image_url VARCHAR(255) DEFAULT NULL
);

-- Orders Table
CREATE TABLE IF NOT EXISTS Orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    items TEXT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    order_status ENUM('In Progress', 'Completed', 'Delivered', 'Cancelled') DEFAULT 'In Progress',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Staffs Table
CREATE TABLE IF NOT EXISTS Staffs (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('Cleaner', 'Waiter', 'Cashier', 'Barista') NOT NULL,
    salary DECIMAL(10,2) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Manager Table
CREATE TABLE IF NOT EXISTS Manager (
    manager_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Default Manager
INSERT INTO Manager (name, password) 
VALUES ('Admin', 'admin123') 
ON DUPLICATE KEY UPDATE password = 'admin123';

-- Sample Staffs
INSERT INTO Staffs (name, username, role, salary, password) 
VALUES 
  ('John Doe', 'john_doe', 'Barista', 15000.00, 'john123'),
  ('Jane Smith', 'jane_smith', 'Waiter', 12000.00, 'jane123'),
  ('Robert Brown', 'robert_brown', 'Cashier', 13000.00, 'robert123') AS new
ON DUPLICATE KEY UPDATE 
  salary = new.salary, 
  password = new.password;


INSERT INTO Menu (item_name, price, image_url)
VALUES
    ('Tea', 20.00, 'https://i.imgur.com/WE06Uf7.jpeg'),
    ('Coffee', 25.00, 'https://i.imgur.com/o93zDNz.png'),
    ('Sandwich', 40.00, 'https://i.imgur.com/cLZoseY.jpeg'),
    ('Pizza', 80.00, 'https://i.imgur.com/CxsShFd.jpeg'),
    ('Burger', 60.00, 'https://i.imgur.com/RtzvtNO.jpeg'),
    ('Noodles', 70.00, 'https://i.imgur.com/fUqepS8.jpeg') AS new
ON DUPLICATE KEY UPDATE
    price = new.price,
    image_url = new.image_url;
  select  * from orders;
  select * from menu;
  

