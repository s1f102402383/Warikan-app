CREATE TABLE mydb.evidences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    text TEXT,
    image_path VARCHAR(255),
    travel_id INT,
    payer_id INT,
    amount INT
);

CREATE TABLE mydb.travels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE mydb.members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    travel_id INT,
    name VARCHAR(255)
);