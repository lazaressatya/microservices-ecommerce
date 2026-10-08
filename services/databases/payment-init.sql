CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) NOT NULL
);

INSERT INTO payments
(order_id, amount, status)
VALUES
(1, 55000.00, 'SUCCESS'),
(2, 50000.00, 'PENDING');