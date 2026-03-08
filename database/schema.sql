-- BusMaster Database Schema
-- SQLite / SQLAlchemy Auto-Generated Reference

CREATE TABLE buses (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_number      VARCHAR(20)  UNIQUE NOT NULL,
    plate_number    VARCHAR(20)  UNIQUE NOT NULL,
    capacity        INTEGER      NOT NULL,
    bus_type        VARCHAR(50)  DEFAULT 'Standard',
    status          VARCHAR(20)  DEFAULT 'Active',  -- Active | Maintenance | Retired
    manufactured_year INTEGER,
    created_at      DATETIME     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE drivers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            VARCHAR(100) NOT NULL,
    license_number  VARCHAR(50)  UNIQUE NOT NULL,
    phone           VARCHAR(20),
    email           VARCHAR(100),
    status          VARCHAR(20)  DEFAULT 'Available', -- Available | On Duty | Off Duty
    hire_date       DATE,
    created_at      DATETIME     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE routes (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    route_name            VARCHAR(100) NOT NULL,
    route_number          VARCHAR(20)  UNIQUE NOT NULL,
    start_location        VARCHAR(200) NOT NULL,
    end_location          VARCHAR(200) NOT NULL,
    start_lat             FLOAT,
    start_lng             FLOAT,
    end_lat               FLOAT,
    end_lng               FLOAT,
    distance_km           FLOAT,
    estimated_duration_min INTEGER,
    status                VARCHAR(20)  DEFAULT 'Active',
    created_at            DATETIME     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bus_stops (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    route_id    INTEGER NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
    stop_name   VARCHAR(100) NOT NULL,
    stop_order  INTEGER      NOT NULL,
    lat         FLOAT,
    lng         FLOAT
);

CREATE TABLE schedules (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    schedule_name   VARCHAR(100) NOT NULL,
    bus_id          INTEGER NOT NULL REFERENCES buses(id),
    driver_id       INTEGER NOT NULL REFERENCES drivers(id),
    route_id        INTEGER NOT NULL REFERENCES routes(id),
    departure_time  VARCHAR(10) NOT NULL,  -- HH:MM
    arrival_time    VARCHAR(10) NOT NULL,  -- HH:MM
    schedule_date   DATE NOT NULL,
    schedule_type   VARCHAR(20) DEFAULT 'Linked',    -- Linked | Unlinked
    status          VARCHAR(20) DEFAULT 'Scheduled', -- Scheduled | In Progress | Completed | Cancelled
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Sample seed data
INSERT INTO buses VALUES (1,'BUS-001','ABC-1234',52,'Standard','Active',2021,datetime('now'));
INSERT INTO buses VALUES (2,'BUS-002','XYZ-5678',45,'Express','Active',2022,datetime('now'));
INSERT INTO buses VALUES (3,'BUS-003','PQR-9012',30,'Mini','Maintenance',2019,datetime('now'));

INSERT INTO drivers VALUES (1,'Ahmad bin Salleh','LIC-001','0123456789','ahmad@tc.gov.my','Available','2020-01-15',datetime('now'));
INSERT INTO drivers VALUES (2,'Lim Wei Ming','LIC-002','0198765432','lim@tc.gov.my','Available','2019-06-01',datetime('now'));
INSERT INTO drivers VALUES (3,'Rajan Pillai','LIC-003','0112233445','rajan@tc.gov.my','On Duty','2021-03-20',datetime('now'));

INSERT INTO routes VALUES (1,'City Centre Express','R-001','Central Terminal','Airport',3.1390,101.6869,3.1200,101.7500,25.5,45,'Active',datetime('now'));
INSERT INTO routes VALUES (2,'Northern Loop','R-002','Chow Kit','Kepong',3.1728,101.6965,3.2000,101.6300,18.2,35,'Active',datetime('now'));
