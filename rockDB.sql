-- Active: 1730235245814@127.0.0.1@3306@rockdb


CREATE DATABASE rockDB;

USE rockDB;

CREATE TABLE images (
    imageID INT AUTO_INCREMENT PRIMARY KEY,
    imageName VARCHAR(255),
    imageData LONGBLOB
);

CREATE TABLE rocks (
    rockID int NOT NULL AUTO_INCREMENT,
    rockName varchar(255) NOT NULL,
    rockClass varchar(255) NOT NULL,
    #mineralComposition varchar(255) NOT NULL,
    RockSubclass varchar(255) NOT NULL,
    #rockDescription varchar(255) NOT NULL,
    imageID int,
    PRIMARY KEY (rockID),
    FOREIGN KEY (imageID) REFERENCES images(imageID)
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

CREATE TABLE posts(
    postID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    postDescription TEXT NOT NUll,
    postUsername VARCHAR(255) FOREIGN KEY postUsername REFERENCES users(userID),
    images VARCHAR(255),
    rockColor ENUM ('Red','Black','White','Green','Yellow','Orange','Blue','Purple'),
    rockID int FOREIGN KEY REFERENCES rocks(rockID)
);


CREATE TABLE users (
    userName varchar(255) NOT NULL,
    userPassword varchar(255),
    fname varchar(255),
    mname varchar(255),
    lname varchar(255),
    postID int,
    FOREIGN KEY (postID) REFERENCES posts(postID)
    PRIMARY KEY (userName)
);

CREATE TABLE posts (
    postID int AUTO_INCREMENT,
    posterUsername varchar(255),
    images int,
    rockColor varchar(255),
    FOREIGN KEY (postID) REFERENCES posts(postID)
    PRIMARY KEY (userName)
);

CREATE TABLE likes (
    userID INT,
    postID INT,
    FOREIGN KEY (userID) REFERENCES users(userID),
    FOREIGN KEY (postID) REFERENCES posts(postID),
    PRIMARY KEY (userID, postID)
);




#INSERT INTO rockTypes (`typeName`)
#VALUES ('Igneous'), ('Sedimentary'), ('Metamorphic');

INSERT INTO images (`imageName`, `imageData`)
VALUES ('Granite', LOAD_FILE('C:\Users\horne\Documents\GitHub\A-Database-That-Rocks\Granite.jpg'));

INSERT INTO minerals (`mineralName`, `mineralHardness`)
VALUES 
('Quartz', 7),
('Feldspar', 6),
('Mica', 2),
('Calcite', 3),
('Hornblende', 5);

INSERT INTO rocks (`rockName`, `class`, , `subClass`)
VALUES ('Granite','Quartz', 'Intrusive igneous rock');

INSERT INTO rocks (`rockName`, `typeID`, `mineralComposition`, `locationFound`, `classification`, `rockDescription`, `imageID`)
VALUES ('Dwayne Johnson', 'Skill', 'Power', );

INSERT INTO users (userName) VALUES ('t');

INSERT INTO users (userName) VALUES ('j');

INSERT INTO userRock (userID, rockID)
VALUES 
(1, 1),
(2, 1),
(1, 2);

#SHOW TABLES;

DROP DATABASE rockDB;

DROP TABLE images

DROP TABLE rocks