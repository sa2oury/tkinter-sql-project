CREATE DATABASE AirlineDB;
USE AirlineDB;

CREATE TABLE Images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    keyword VARCHAR(100) UNIQUE NOT NULL, 
    image_data LONGBLOB NOT NULL,         
    filename VARCHAR(255) NOT NULL
);

CREATE TABLE Passenger (
    passenger_id INT PRIMARY KEY,
    name VARCHAR(100),
    passport_number VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE Employee (
    employee_id INT PRIMARY KEY,
    name VARCHAR(100),
    role VARCHAR(50),
    salary DECIMAL(10,2)
);

CREATE TABLE Airport (
    airport_id INT PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50),
    code VARCHAR(10)
);

CREATE TABLE Aircraft (
    aircraft_id INT PRIMARY KEY,
    model VARCHAR(50),
    total_seats INT
);

CREATE TABLE Flight (
    flight_id INT PRIMARY KEY,
    flight_number VARCHAR(20),
    departure_airport_id INT,
    arrival_airport_id INT,
    departure_time DATETIME,
    arrival_time DATETIME,
    aircraft_id INT,
    FOREIGN KEY (departure_airport_id) REFERENCES Airport(airport_id),
    FOREIGN KEY (arrival_airport_id) REFERENCES Airport(airport_id),
    FOREIGN KEY (aircraft_id) REFERENCES Aircraft(aircraft_id)
);

CREATE TABLE Ticket (
    ticket_id INT PRIMARY KEY,
    passenger_id INT,
    flight_id INT,
    seat_number VARCHAR(10),
    price DECIMAL(10,2),
    booking_date DATETIME,
    FOREIGN KEY (passenger_id) REFERENCES Passenger(passenger_id),
    FOREIGN KEY (flight_id) REFERENCES Flight(flight_id)
);

INSERT INTO Passenger (passenger_id, name, passport_number, phone, email) VALUES
(1, 'Ahmed Ali', 'P123456', '0100000001', 'ahmed@mail.com'),
(2, 'Sara Mohamed', 'P234567', '0100000002', 'sara@mail.com'),
(3, 'Omar Hassan', 'P345678', '0100000003', 'omar@mail.com'),
(4, 'Mona Adel', 'P456789', '0100000004', 'mona@mail.com');

INSERT INTO Employee (employee_id, name, role, salary) VALUES
(1, 'Captain Ali', 'Pilot', 20000),
(2, 'Nour Ahmed', 'Crew', 8000),
(3, 'Hany Samy', 'Admin', 6000),
(4, 'Salma Hassan', 'Crew', 8500);

INSERT INTO Airport (airport_id, name, city, country, code) VALUES
(1, 'Cairo International Airport', 'Cairo', 'Egypt', 'CAI'),
(2, 'Dubai International Airport', 'Dubai', 'UAE', 'DXB'),
(3, 'JFK Airport', 'New York', 'USA', 'JFK'),
(4, 'Heathrow Airport', 'London', 'UK', 'LHR');

INSERT INTO Aircraft (aircraft_id, model, total_seats) VALUES
(1, 'Boeing 737-800', 180),
(2, 'Airbus A320', 170),
(3, 'Boeing 777-300', 300),
(4, 'Airbus A380', 500);

INSERT INTO Flight (flight_id, flight_number, departure_airport_id, arrival_airport_id, departure_time, arrival_time, aircraft_id) VALUES
(1, 'MS101', 1, 2, '2026-05-01 10:00:00', '2026-05-01 14:00:00', 1),
(2, 'MS102', 2, 1, '2026-05-02 12:00:00', '2026-05-02 16:00:00', 2),
(3, 'MS103', 1, 3, '2026-05-03 08:00:00', '2026-05-03 18:00:00', 3),
(4, 'MS104', 3, 1, '2026-05-04 09:00:00', '2026-05-04 19:00:00', 1);

INSERT INTO Ticket (ticket_id, passenger_id, flight_id, seat_number, price, booking_date) VALUES
(1, 1, 1, 'A1', 2000, '2026-04-20'),
(2, 2, 2, 'B2', 2500, '2026-04-21'),
(3, 3, 3, 'C3', 3000, '2026-04-22'),
(4, 1, 2, 'A2', 2200, '2026-04-23');

UPDATE Ticket SET seat_number = 'A10' WHERE ticket_id = 1;
UPDATE Ticket SET price = 2600 WHERE ticket_id = 2;
UPDATE Ticket SET booking_date = '2026-04-25' WHERE ticket_id = 3;
UPDATE Ticket SET passenger_id = 2 WHERE ticket_id = 4;

DELETE FROM Ticket WHERE ticket_id = 4;