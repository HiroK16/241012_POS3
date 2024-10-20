CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code CHAR(13) UNIQUE,
    name VARCHAR(50),
    price FLOAT
);

CREATE TABLE purchases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    total FLOAT
);

