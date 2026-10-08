CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    username VARCHAR(100) NOT NULL,
    rating INT NOT NULL,
    comment VARCHAR(500)
);

INSERT INTO reviews
(product_id, username, rating, comment)
VALUES
(1, 'John', 5, 'Excellent product'),
(2, 'David', 4, 'Good product');