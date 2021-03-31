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
	ISO CHAR(3) NOT NULL PRIMARY KEY,
	Nom varchar(30) UNIQUE,
	hdi float,
	Population BIGINT,
	Region varchar(30) NOT NULL CONSTRAINT region_fk REFERENCES Region(nom),
	climat SERIAL CONSTRAINT climat_fk REFERENCES Climat(id)
);

CREATE TABLE Vaccins (
	Nom varchar(40) NOT NULL PRIMARY KEY
);

CREATE TABLE CampagneVaccin (
	NomVaccin varchar(40) NOT NULL CONSTRAINT nomvaccin_fk REFERENCES Vaccins(nom),
	Iso_pays CHAR(3) NOT NULL CONSTRAINT isopays_fk REFERENCES Pays(ISO),
	CONSTRAINT vaccin_pk PRIMARY KEY (NomVaccin, Iso_pays)
);

CREATE TABLE Utilisateur (
	id INT NOT NULL PRIMARY KEY,
	Nom varchar(40),
	Prenom varchar(40),
	pseudo varchar(40) NOT NULL ,
	motdepasse varchar(40) NOT NULL ,
	RueAdresse varchar(100),
	CodePostalAdresse INT,
	NumeroAdresse INT,
	VilleAdresse varchar(40)
);

CREATE TABLE Epidemiologiste (
	id int NOT NULL CONSTRAINT idepidemiologiste_fk REFERENCES Utilisateur(id),
	centre varchar(40),
	telephoneservice varchar(20),
	CONSTRAINT idepidemiologiste_pk PRIMARY KEY (id)
);

CREATE TABLE StatsJournalieres (
	IsoPays char(3) NOT NULL CONSTRAINT isopays_fk REFERENCES Pays(ISO),
	date DATE NOT NULL,
	test BIGINT,
	vaccinations BIGINT,
	Icu_patiens BIGINT,
	hosp_patiens BIGINT,
	IdEpi int CONSTRAINT idepi_fk REFERENCES Epidemiologiste(id),
	CONSTRAINT stats_pk PRIMARY KEY(IsoPays, date),
	CONSTRAINT icu_hosp CHECK (Icu_patiens <= hosp_patiens),
	CONSTRAINT icu_hosp_nul CHECK (Icu_patiens = 0 AND hosp_patiens != 0),
	CONSTRAINT icu_hosp_nul2 CHECK (Icu_patiens != 0 AND hosp_patiens = 0)
);