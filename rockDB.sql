-- Active: 1725994447906@127.0.0.1@3306@rockdb


CREATE DATABASE rockDB;

USE rockDB;

CREATE TABLE rockTypes (
    typeID int NOT NULL AUTO_INCREMENT,
    typeName varchar(255) NOT NULL,
    PRIMARY KEY (typeID)
);

CREATE TABLE rocks (
    rockID int NOT NULL AUTO_INCREMENT,
    rockName varchar(255) NOT NULL,
    typeID int NOT NULL,
    mineralComposition varchar(255) NOT NULL,
    locationFound varchar(255) NOT NULL,
    classification varchar(255) NOT NULL,
    rockDescription varchar(255) NOT NULL,
    PRIMARY KEY (rockID),
    FOREIGN KEY (typeID) REFERENCES rockTypes(typeID)
);



CREATE TABLE minerals (
    mineralID int NOT NULL AUTO_INCREMENT,
    mineralName varchar(255) NOT NULL,
    mineralHardness int ,
    PRIMARY KEY (mineralID)
);

CREATE TABLE rockMineral (
    rockID int,
    mineralID int,
    FOREIGN KEY (rockID) REFERENCES rocks(rockID),
    FOREIGN KEY (mineralID) REFERENCES minerals(mineralID),
    PRIMARY KEY (rockID, mineralID)
);



CREATE TABLE users (
    userID int NOT NULL AUTO_INCREMENT,
    userName varchar(255),
    PRIMARY KEY (userID)
);

CREATE TABLE userRock (
    userID INT,
    rockID INT,
    FOREIGN KEY (userID) REFERENCES users(userID),
    FOREIGN KEY (rockID) REFERENCES rocks(rockID),
    PRIMARY KEY (userID, rockID)
);

INSERT INTO rockTypes (`typeName`)
VALUES ('Igneous'), ('Sedimentary'), ('Metamorphic');

INSERT INTO minerals (`mineralName`, `mineralHardness`)
VALUES 
('Quartz', 7),
('Feldspar', 6),
('Mica', 2),
('Calcite', 3),
('Hornblende', 5);

INSERT INTO rocks (`rockName`, `typeID`, `mineralComposition`, `locationFound`, `classification`, `rockDescription`)
VALUES ('Granite', 1, 'Quartz, Feldspar, Mica', 'Colorado, USA', 'Intrusive igneous rock', 'A rock that is equal parts Gran and ite');

INSERT INTO rocks (`rockName`, `typeID`, `mineralComposition`, `locationFound`, `classification`, `rockDescription`)
VALUES ('Dwayne Johnson', 3, 'Skill, Power, Glare', 'In your dreams', 'Smouldering', 'He has a son named, "The Pebble"');

INSERT INTO userRock (userID, rockID)
VALUES 
(1, 1),
(2, 1),
(1, 2);

#SHOW TABLES;

#DROP DATABASE rockDB;

DROP TABLE userRock

DROP TABLE users