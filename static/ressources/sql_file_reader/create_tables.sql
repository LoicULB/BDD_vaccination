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
	Region varchar(50) CONSTRAINT region_fk REFERENCES Region(nom),
	Nom varchar(50) UNIQUE,
	hdi float,
	Population BIGINT,
	Surface BIGINT,
	
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
	id SERIAL NOT NULL PRIMARY KEY,
	uuid uuid NOT NULL UNIQUE,
	Nom varchar(40),
	Prenom varchar(40),
	pseudo varchar(40) UNIQUE , --should be not null
	mot_de_passe varchar(100)  , --should be not null
	rue_Adresse varchar(100),
	code_postal_adresse INT,
	numero_adresse INT,
	ville_adresse varchar(40)
	CONSTRAINT adresse_integrity_constraint CHECK (((rue_adresse is NULL)::int + (rue_adresse is NULL)::int +(code_postal_adresse is NULL)::int + (numero_adresse is NULL)::int )in (0,4))
	--rajouter contrainte d'intégrité sur chaque colonne adresse
	
	--ALTER TABLE utilisateur ADD CONSTRAINT adresse_integrity_constraint CHECK (((rue_adresse is NULL)::int + (rue_adresse is NULL)::int +(code_postal_adresse is NULL)::int + (numero_adresse is NULL)::int )in (0,4))
);

CREATE TABLE Epidemiologiste (
	--id int NOT NULL PRIMARY KEY CONSTRAINT idepidemiologiste_fk REFERENCES Utilisateur(uuid),
	uuid uuid NOT NULL Unique CONSTRAINT idepidemiologiste_fk REFERENCES Utilisateur(uuid) ON DELETE CASCADE,
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
	test BIGINT,
	vaccinations BIGINT,

	CONSTRAINT Vaccinnations_pk PRIMARY KEY(id)
);

CREATE TABLE hospitalisations_stats (
	id INT NOT NULL CONSTRAINT idvaccination_fk REFERENCES Stats_Journalieres(id),
	Icu_patiens BIGINT,
	hosp_patiens BIGINT,
	CONSTRAINT patients_integrity CHECK (((icu_patiens is NOT NULL)::int + (hosp_patiens is NOT NULL)::int) IN (0,2)),
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

CREATE OR REPLACE FUNCTION auto_insert_pays() RETURNS TRIGGER
LANGUAGE PLPGSQL AS $$
BEGIN

	IF NOT EXISTS (SELECT iso FROM pays WHERE iso=NEW.iso_pays) THEN
		INSERT INTO pays(iso) VALUES (NEW.iso_pays);
	END IF;
	RETURN NEW;
END; $$;

CREATE TRIGGER auto_insert_pays BEFORE INSERT ON campagne_vaccin FOR EACH ROW 
EXECUTE PROCEDURE auto_insert_pays();
CREATE TRIGGER auto_insert_pays BEFORE INSERT ON stats_journalieres FOR EACH ROW 
EXECUTE PROCEDURE auto_insert_pays();

CREATE TRIGGER auto_insert_user BEFORE INSERT ON epidemiologiste FOR EACH ROW 
EXECUTE PROCEDURE auto_insert_user();

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
INSERT INTO utilisateur(uuid, pseudo, mot_de_passe) VALUES (uuid_generate_v4(), 'Harry', $$Caput Draconis$$);



----
CREATE OR REPLACE FUNCTION stats_journalieres_date_after_start_campaign() RETURNS TRIGGER 
LANGUAGE PLPGSQL AS $$
DECLARE
   date_vs stats_journalieres.date%type;
   date_start_campaign pays.debut_vaccination%type;
BEGIN
	SELECT date
	FROM stats_journalieres s
	INTO date_vs
	WHERE s.id=NEW.id;
	raise notice 'Date VS :  %s', date_vs;

	SELECT debut_vaccination
	FROM pays p 
	JOIN stats_journalieres s ON p.iso=s.iso_pays
	INTO date_start_campaign
	WHERE s.id=NEW.id;
	raise notice 'Date Start Campaign :  %s', date_vs;

	IF(NEW.vaccinations is NOT NULL AND date_vs < date_start_campaign) THEN
		RAISE EXCEPTION 'La date de la stat journaliere doit etre posterieure à la date de debut de vaccination du pays concerne';
	END IF;
	RETURN NEW;
END; $$;
-----
CREATE TRIGGER stats_journalieres_date_after_start_campaign 
BEFORE INSERT OR UPDATE OF vaccinations ON vaccinnations_stats FOR EACH ROW 
EXECUTE PROCEDURE stats_journalieres_date_after_start_campaign();
------
--we could add check on pays and stats_journalieres on update or insert of date but it would be long
-----

--INSERT INTO vaccinnations_stats(id, vaccinations) VALUES (1, 1000)

--SELECT sj.id 
--FROM stats_journalieres sj JOIN pays p ON p.iso=sj.iso_pays
--WHERE debut_vaccination < date

--UPDATE vaccinnations_stats SET vaccinations=1000 WHERE id=6279

--
--SELECT sj.id 
--FROM stats_journalieres sj NATURAL JOIN vaccinnations_stats JOIN pays p ON p.iso=sj.iso_pays
--WHERE debut_vaccination > date
--
--