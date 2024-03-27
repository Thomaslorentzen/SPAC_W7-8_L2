CREATE TABLE `kategori` (
  `kategori_ID` int NOT NULL AUTO_INCREMENT,
  `kategori_navn` varchar(255) DEFAULT NULL,
  `beskrivelse` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`kategori_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
DELIMITER $$

CREATE TABLE `transaktioner` (
  `transaktion_ID` int NOT NULL AUTO_INCREMENT,
  `vare_ID` int DEFAULT NULL,
  `dato_og_tid` datetime NOT NULL,
  `antal` int DEFAULT NULL,
  `transaktionstype` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`transaktion_ID`),
  KEY `vare_ID` (`vare_ID`),
  CONSTRAINT `transaktioner_ibfk_1` FOREIGN KEY (`vare_ID`) REFERENCES `vare` (`vare_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `vare` (
  `vare_ID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `beskrivelse` varchar(255) DEFAULT NULL,
  `kategori_ID` int NOT NULL,
  `pris` int DEFAULT NULL,
  `lager_antal` int DEFAULT NULL,
  PRIMARY KEY (`vare_ID`),
  KEY `fk_kategori_id` (`kategori_ID`),
  CONSTRAINT `fk_kategori_id` FOREIGN KEY (`kategori_ID`) REFERENCES `kategori` (`kategori_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- stored procedures
CREATE DEFINER=`root`@`localhost` PROCEDURE `FjernKategori`(
    IN p_kategori_ID INT
)
BEGIN
    DELETE FROM kategori WHERE kategori_ID = p_kategori_ID;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `FjernVare`(
    IN p_vare_ID INT
)
BEGIN
    DELETE FROM vare WHERE vare_ID = p_vare_ID;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `HentKategoriInfo`(
    IN p_kategori_ID INT
)
BEGIN
    SELECT * FROM kategori WHERE kategori_ID = p_kategori_ID;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `HentTransaktionInfo`(
    IN p_transaktion_ID INT
)
BEGIN
    SELECT * FROM Transaktioner WHERE TransaktionID = p_transaktion_ID;
END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `HentVareInfo`(
    IN p_vare_ID INT
)
BEGIN
    SELECT * FROM vare WHERE vare_ID = p_vare_ID;
END$$
DELIMITER ;
DELIMITER $$

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `OpdaterKategori`(
    IN p_kategori_ID INT,
    IN p_kategori_navn VARCHAR(255),
    IN p_beskrivelse VARCHAR(255)
)
BEGIN
    UPDATE kategori
    SET kategori_navn = p_kategori_navn, beskrivelse = p_beskrivelse
    WHERE kategori_ID = p_kategori_ID;
END$$
DELIMITER ;


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `OpdaterVare`(
IN p_vare_ID INT,
    IN p_name VARCHAR(255),
    IN p_beskrivelse VARCHAR(255),
    IN p_kategori_ID INT,
    IN p_pris INT,
    IN p_lager_antal INT
)

BEGIN
    UPDATE vare
    SET name = p_name, beskrivelse = p_beskrivelse, kategori_ID = p_kategori_ID, pris = p_pris, lager_antal = p_lager_antal
    WHERE vare_ID = p_vare_ID;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `OpretTransaktion`(
    IN p_vare_id INT,
    IN p_dato_og_tid DATETIME,
    IN p_transaktionstype VARCHAR(50),
    IN p_antal INT
)
BEGIN
    -- Insert a new transaction into the 'transaktioner' table
    INSERT INTO transaktioner (vare_id, dato_og_tid, transaktionstype, antal)
    VALUES (p_vare_id, p_dato_og_tid, p_transaktionstype, p_antal);
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `TilføjKategori`(
   IN kategori_navn VARCHAR(255),
    IN beskrivelse VARCHAR(255)
)
BEGIN
    INSERT INTO kategori (kategori_navn, beskrivelse)
    VALUES (kategori_navn, beskrivelse);
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `TilføjVare`(
    IN name VARCHAR(255),
    IN beskrivelse TEXT,
    IN kategori_ID INT,
    IN pris DECIMAL(10, 2),
    IN lager_antal INT
)
BEGIN
    INSERT INTO vare (name, beskrivelse, kategori_ID, pris, lager_antal)
    VALUES (name, beskrivelse, kategori_ID, pris, lager_antal);
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `SøgEfterVare`(IN vare_navn VARCHAR(255))
BEGIN
    -- Convert input to lowercase for case-insensitive search
    SET vare_navn = LOWER(vare_navn); 
    
    -- Search for items that match the input name partially or fully
    SELECT * FROM Vare WHERE LOWER(name) LIKE CONCAT('%', vare_navn, '%');
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `SøgEfterKategori`(IN kategori_navn VARCHAR(255))
BEGIN

    SET kategori_navn = LOWER(kategori_navn); -- Convert input to lowercase for case-insensitive search
    
    -- Search for categories that match the input name partially or fully
    SELECT * FROM Kategori WHERE LOWER(navn) LIKE CONCAT('%', kategori_navn, '%');
END$$
DELIMITER ;

