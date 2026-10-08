CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    status VARCHAR(50) NOT NULL
);

INSERT INTO orders
(product, quantity, status)
VALUES
('Laptop', 1, 'CONFIRMED'),
('Mobile', 2, 'PROCESSING');