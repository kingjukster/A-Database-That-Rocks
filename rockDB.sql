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
    rockSubclass varchar(255),
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

CREATE TABLE users (
    userID int AUTO_INCREMENT,
    userPassword varchar(255),
    fName varchar(255) NOT NULL,
    mName varchar(255),
    lName varchar(255) NOT NULL,
    #postID int,
    #FOREIGN KEY (postID) REFERENCES posts(postID)
    PRIMARY KEY (userID)
);

CREATE TABLE posts(
    postID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    postDescription TEXT NOT NUll,
    postUserID int,
    images VARCHAR(255),
    rockColor ENUM ('Black', 'Blue', 'Green', 'Orange', 'Purple', 'Red', 'White', 'Yellow'),
    rockID int,
    likes int,
    FOREIGN KEY (postUserID) REFERENCES users(userID),
    FOREIGN KEY (rockID) REFERENCES rocks(rockID)
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





INSERT INTO users (userPassword, fName, mName, lName) VALUES ('579d9814911e70768fa01ae064b1566f', 'ADMIN', NULL, 'l'), ('0', 'Terrell', 'Michael', 'Heredia'), ('579d9814911e70768fa01ae064b1566f', 'ADMIN', NULL, 'ADMIN');




