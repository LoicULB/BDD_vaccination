CREATE TABLE Continent (
	Nom varchar(20) NOT NULL PRIMARY KEY
);

CREATE TABLE Region (
	Nom varchar(30) NOT NULL PRIMARY KEY,
	nom_continent varchar(20) NOT NULL CONSTRAINT continent_fk REFERENCES Continent(nom)
);

CREATE TABLE Climat (
	id SERIAL NOT NULL PRIMARY KEY,
	description varchar(200) NOT NULL 
	
);

CREATE TABLE Pays (
	ISO varchar(15) NOT NULL PRIMARY KEY,
	Region varchar(50) NOT NULL CONSTRAINT region_fk REFERENCES Region(nom),
	Nom varchar(50) UNIQUE,
	hdi float,
	Surface BIGINT,
	Population BIGINT,
	climat INT CONSTRAINT climat_fk REFERENCES Climat(id),
	debut_vaccination DATE 
	
	
);

CREATE TABLE Vaccins (
	Nom varchar(40) NOT NULL PRIMARY KEY
);

CREATE TABLE Campagne_Vaccin (
	Iso_pays VARCHAR(15) NOT NULL CONSTRAINT isopays_fk REFERENCES Pays(ISO),
	Nom_Vaccin varchar(40) NOT NULL CONSTRAINT nomvaccin_fk REFERENCES Vaccins(nom),
	
	CONSTRAINT vaccin_pk PRIMARY KEY (Nom_Vaccin, Iso_pays)
);
-- 


--
CREATE TABLE Utilisateur (
	--id SERIAL NOT NULL PRIMARY KEY,
	uuid uuid NOT NULL PRIMARY KEY,
	Nom varchar(40),
	Prenom varchar(40),
	pseudo varchar(40)  , --should be not null
	mot_de_passe varchar(40)  , --should be not null
	rue_Adresse varchar(100),
	code_postal_adresse INT,
	numero_adresse INT,
	ville_adresse varchar(40)
);

CREATE TABLE Epidemiologiste (
	--id int NOT NULL CONSTRAINT idepidemiologiste_fk REFERENCES Utilisateur(uuid),
	uuid uuid NOT NULL PRIMARY KEY CONSTRAINT idepidemiologiste_fk REFERENCES Utilisateur(uuid),
	centre varchar(40),
	telephone_service varchar(20)
);

CREATE TABLE Stats_Journalieres (
	id INT NOT NULL PRIMARY KEY,
	Iso_Pays varchar(15) NOT NULL CONSTRAINT isopays_fk REFERENCES Pays(ISO),
	date DATE NOT NULL,
	Id_Epi uuid CONSTRAINT idepi_fk REFERENCES Epidemiologiste(uuid),
	CONSTRAINT datepays_unique UNIQUE (date, Iso_Pays)
);

CREATE TABLE Vaccinnations_stats (
	id INT NOT NULL CONSTRAINT idvaccination_fk REFERENCES Stats_Journalieres(id),
	vaccinations BIGINT,
	test BIGINT,
	CONSTRAINT Vaccinnations_pk PRIMARY KEY(id)
);

CREATE TABLE hospitalisations_stats (
	id INT NOT NULL CONSTRAINT idvaccination_fk REFERENCES Stats_Journalieres(id),
	Icu_patiens BIGINT,
	hosp_patiens BIGINT,
	CONSTRAINT icu_hosp CHECK (Icu_patiens <= hosp_patiens),
	CONSTRAINT hospitalisations_pk PRIMARY KEY(id)
);

--Pull my devil trigger
CREATE OR REPLACE FUNCTION auto_insert_user() RETURNS TRIGGER 
LANGUAGE PLPGSQL AS $$
BEGIN
	INSERT INTO utilisateur(uuid) VALUES (NEW.uuid);
	RETURN NEW;
END; $$;

CREATE TRIGGER auto_insert_user BEFORE INSERT ON epidemiologiste FOR EACH ROW 
EXECUTE PROCEDURE auto_insert_user();