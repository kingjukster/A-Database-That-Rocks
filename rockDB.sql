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
    --mineralComposition varchar(255) NOT NULL,
    rockSubclass varchar(255),
    --rockDescription varchar(255) NOT NULL,
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
    --postID int,
    --FOREIGN KEY (postID) REFERENCES posts(postID)
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




--INSERT INTO rockTypes (`typeName`)
--VALUES ('Igneous'), ('Sedimentary'), ('Metamorphic');

INSERT INTO images (`imageName`, `imageData`)
VALUES ('Granite', LOAD_FILE('C:\Users\horne\Documents\GitHub\A-Database-That-Rocks\Granite.jpg'));

INSERT INTO minerals (`mineralName`, `mineralHardness`)
VALUES 
('Alkali feldspar', 6),
('Apatite', 5),
('Biotite', 3),
('Calcite', 3),
('Carbon', 2),
('Chlorite', 2),
('Clay minerals', 2),
('Dolomite', 4),
('Feldspar', 6),
('Feldspathoid', 6),
('Garnet', 7),
('Glaucophane', 6),
('Hematite', 6),
('Hornblende', 6),
('Iron oxides', 6),
('Kyanite', 6),
('Muscovite', 2),
('Nepheline', 6),
('Olivine', 7),
('Orthopyroxene', 6),
('Phlogopite', 3),
('Plagioclase', 6),
('Pyroxene', 6),
('Quartz', 7),
('Serpentine', 3),
('Silica', 7),
('Sylvite', 2),
('Talc', 1);

drop table minerals

drop table rockmineral

INSERT INTO rockmineral(`rockID`,`mineralID`)
VALUES
(1, 22),  -- Adakite: Plagioclase
    (2, 22),  -- Andesite: Plagioclase
    (3, 9),   -- Alkali: Feldspar
    (4, 22),  -- Anorthosite: Plagioclase
    (5, 24),  -- Aplite: Quartz
    (6, 23),  -- Basalt: Pyroxene
    (7, 19),  -- Aā: Olivine
    (8, 19),  -- Pāhoehoe: Olivine
    (9, 23),  -- Basaltic: Pyroxene
    (10, 9),  -- Mugearite: Feldspar
    (11, 9),  -- Shoshonite: Feldspar
    (12, 19), -- Basanite: Olivine
    (13, 18), -- Blairmorite: Nepheline
    (14, 23), -- Boninite: Pyroxene
    (15, 4),  -- Carbonatite: Calcite
    (16, 20), -- Charnockite: Orthopyroxene
    (17, 22), -- Enderbite: Plagioclase
    (18, 24), -- Dacite: Quartz
    (19, 22), -- Diabase: Plagioclase
    (20, 22), -- Diorite: Plagioclase
    (21, 22), -- Napoleonite: Plagioclase
    (22, 19), -- Dunite: Olivine
    (23, 18), -- Essexite: Nepheline
    (24, 10), -- Foidolite: Feldspathoid
    (25, 23), -- Gabbro: Pyroxene
    (26, 24), -- Granite: Quartz
    (27, 24), -- Granodiorite: Quartz
    (28, 24), -- Granophyre: Quartz
    (29, 19), -- Harzburgite: Olivine
    (30, 14), -- Hornblendite: Hornblende
    (31, 24), -- Hyaloclastite: Quartz
    (32, 22), -- Icelandite: Plagioclase
    (33, 24), -- Ignimbrite: Quartz
    (34, 18), -- Ijolite: Nepheline
    (35, 19), -- Kimberlite: Olivine
    (36, 19), -- Komatiite: Olivine
    (37, 20), -- Lamproite: Orthopyroxene
    (38, 3),  -- Lamprophyre: Biotite
    (39, 9),  -- Latite: Feldspar
    (40, 19), -- Lherzolite: Olivine
    (41, 24), -- Monzogranite: Quartz
    (42, 22), -- Monzonite: Plagioclase
    (43, 18), -- Nepheline: Nepheline
    (44, 18), -- Nephelinite: Nepheline
    (45, 22), -- Norite: Plagioclase
    (46, 24), -- Obsidian: Quartz
    (47, 24), -- Pegmatite: Quartz
    (48, 19), -- Peridotite: Olivine
    (49, 18), -- Phonolite: Nepheline
    (50, 18), -- Phonotephrite: Nepheline
    (51, 19), -- Picrite: Olivine
    (52, 24), -- Porphyry: Quartz
    (53, 24), -- Pumice: Quartz
    (54, 23), -- Pyroxenite: Pyroxene
    (55, 24), -- Quartzolite: Quartz
    (56, 24), -- Rhyodacite: Quartz
    (57, 24), -- Rhyolite: Quartz
    (58, 24), -- Comendite: Quartz
    (59, 9),  -- Pantellerite: Feldspar
    (60, 23), -- Scoria: Pyroxene
    (61, 18), -- Shonkinite: Nepheline
    (62, 4),  -- Sovite: Calcite
    (63, 9),  -- Syenite: Feldspar
    (64, 28), -- Tachylyte: Glass
    (65, 18), -- Tephriphonolite: Nepheline
    (66, 18), -- Tephrite: Nepheline
    (67, 22), -- Tonalite: Plagioclase
    (68, 9),  -- Trachyandesite: Feldspar
    (69, 9),  -- Benmoreite: Feldspar
    (70, 9),  -- Trachybasalt: Feldspar
    (71, 9),  -- Hawaiite: Feldspar
    (72, 1),  -- Trachyte: Alkali feldspar
    (73, 22), -- Troctolite: Plagioclase
    (74, 24), -- Trondhjemite: Quartz
    (75, 24), -- Tuff: Quartz
    (76, 23), -- Websterite: Pyroxene
    (77, 19), -- Wehrlite: Olivine
    (78, 7),   -- Argillite: Clay minerals
    (79, 9),   -- Arkose: Feldspar
    (80, 24),  -- Banded: Quartz
    (81, 24),  -- Breccia: Quartz
    (82, 4),   -- Calcarenite: Calcite
    (83, 4),   -- Chalk: Calcite
    (84, 24),  -- Chert: Quartz
    (85, 7),   -- Claystone: Clay minerals
    (86, 5),   -- Coal: Carbon
    (87, 24),  -- Conglomerate: Quartz
    (88, 4),   -- Coquina: Calcite
    (89, 24),  -- Diamictite: Quartz
    (90, 24),  -- Diatomite: Quartz
    (91, 7),   -- Dolomite: Dolomite
    (92, 4),   -- Evaporite: Calcite
    (93, 24),  -- Flint: Quartz
    (94, 24),  -- Geyserite: Quartz
    (95, 7),   -- Greywacke: Clay minerals
    (96, 24),  -- Gritstone: Quartz
    (97, 24),  -- Itacolumite: Quartz
    (98, 24),  -- Jaspillite: Quartz
    (99, 5),   -- Laterite: Carbon
    (100, 5),  -- Lignite: Carbon
    (101, 4),  -- Limestone: Calcite
    (102, 7),  -- Marl: Clay minerals
    (103, 7),  -- Mudstone: Clay minerals
    (104, 5),  -- Oil: Carbon
    (105, 4),  -- Oolite: Calcite
    (106, 4),  -- Phosphorite: Calcite
    (107, 24), -- Sandstone: Quartz
    (108, 7),  -- Shale: Clay minerals
    (109, 7),  -- Siltstone: Clay minerals
    (110, 27), -- Sylvinite: Sylvite
    (111, 24), -- Tillite: Quartz
    (112, 4),  -- Travertine: Calcite
    (113, 4),  -- Tufa: Calcite
    (114, 24), -- Turbidite: Quartz
    (115, 24),-- Wackestone: Quartz
    (116, 5),  -- Anthracite: Carbon
    (117, 14), -- Amphibolite: Hornblende
    (118, 12), -- Blueschist: Glaucophane
    (119, 24), -- Cataclasite: Quartz
    (120, 11), -- Eclogite: Garnet
    (121, 24), -- Gneiss: Quartz
    (122, 24), -- Granulite: Quartz
    (123, 7),  -- Greenschist: Clay minerals
    (124, 24), -- Hornfels: Quartz
    (125, 4),  -- Calcflinta: Calcite
    (126, 24), -- Litchfieldite: Quartz
    (127, 4),  -- Marble: Calcite
    (128, 24), -- Migmatite: Quartz
    (129, 24), -- Mylonite: Quartz
    (130, 7),  -- Metapelite: Clay minerals
    (131, 24), -- Metapsammite: Quartz
    (132, 24), -- Phyllite: Quartz
    (133, 24), -- Pseudotachylite: Quartz
    (134, 24), -- Quartzite: Quartz
    (135, 24), -- Schist: Quartz
    (136, 26), -- Serpentinite: Serpentine
    (137, 24), -- Skarn: Quartz
    (138, 24), -- Slate: Quartz
    (139, 24), -- Suevite: Quartz
    (140, 28), -- Talc: Talc
    (141, 28), -- Soapstone: Talc
    (142, 24), -- Tectonite: Quartz
    (143, 24); -- Whiteschist: Quartz


INSERT INTO rockmineral(`rockID`,`mineralID`)
VALUES
(26,1)


INSERT INTO posts (`postDescription`, `postUserID`, `images`, `rockColor`, `rockID`)
VALUES 
('This is rock', 2, 'C:/Users/Terrell/database/A-Database-That-Rocks/Granite.jpg', 'Red', 1),
('This is rock', 2, 'C:/Users/horne/Pictures/Cyberpunk 2077/photomode_07022024_001749.png', 'Black', 1)

INSERT INTO users (userPassword, fName, mName, lName) VALUES ('p', 'ADMIN', NULL, 'l'), ('0', 'Terrell', 'Michael', 'Heredia');
INSERT INTO likes (userID,postID) VALUES (1,1);
DELETE from likes WHERE userID =1 AND postID = 1 ;



SELECT * FROM posts ORDER BY rockColor 

--SHOW TABLES;

DROP DATABASE rockDB;

DROP TABLE images

DROP TABLE rocks