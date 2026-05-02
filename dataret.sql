-- 2. Recreate the database and use it
CREATE DATABASE ImageDatabase;
USE ImageDatabase;

-- 3. Create a single, simple table just for storing images
CREATE TABLE Images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    keyword VARCHAR(100) UNIQUE NOT NULL, 
    image_data LONGBLOB NOT NULL,         
    filename VARCHAR(255) NOT NULL
);