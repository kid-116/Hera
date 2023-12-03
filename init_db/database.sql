DROP DATABASE IF EXISTS hera;
CREATE DATABASE hera;

CREATE TABLE hera.users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50),
    phone VARCHAR(10),
    password VARCHAR(100)
);

CREATE TABLE hera.friends (
	id1 INT,
	id2 INT,
	balance INT
);

CREATE TABLE hera.history (
	id1 INT,
	id2 INT,
	amount INT,
	description VARCHAR(100),
	dateAdded DATE
);

CREATE TABLE hera.groups (
	id INT AUTO_INCREMENT PRIMARY KEY,
	size INT,
	name VARCHAR(100)
);

CREATE TABLE hera.group_data (
	id INT,
	group_id INT
);

CREATE TABLE hera.group_transactions (
	id INT,
	amount INT,
	group_id INT,
	description VARCHAR(100),
	dateAdded DATE
);
