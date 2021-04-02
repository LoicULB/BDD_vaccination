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
	Nom varchar(30) UNIQUE,
	hdi float,
	Surface BIGINT,
	Population BIGINT,
	debut_vaccination DATE NOT NULL,
	Region varchar(30) NOT NULL CONSTRAINT region_fk REFERENCES Region(nom),
	climat SERIAL CONSTRAINT climat_fk REFERENCES Climat(id)
);

CREATE TABLE Vaccins (
	Nom varchar(40) NOT NULL PRIMARY KEY
);

CREATE TABLE Campagne_Vaccin (
	Nom_Vaccin varchar(40) NOT NULL CONSTRAINT nomvaccin_fk REFERENCES Vaccins(nom),
	Iso_pays CHAR(3) NOT NULL CONSTRAINT isopays_fk REFERENCES Pays(ISO),
	CONSTRAINT vaccin_pk PRIMARY KEY (Nom_Vaccin, Iso_pays)
);

CREATE TABLE Utilisateur (
	id INT NOT NULL PRIMARY KEY,
	Nom varchar(40),
	Prenom varchar(40),
	pseudo varchar(40) NOT NULL ,
	mot_de_passe varchar(40) NOT NULL ,
	Rue_Adresse varchar(100),
	Code_Postal_Adresse INT,
	Numero_Adresse INT,
	Ville_Adresse varchar(40)
);

CREATE TABLE Epidemiologiste (
	id int NOT NULL CONSTRAINT idepidemiologiste_fk REFERENCES Utilisateur(id),
	centre varchar(40),
	telephone_service varchar(20),
	CONSTRAINT idepidemiologiste_pk PRIMARY KEY (id)
);

CREATE TABLE Stats_Journalieres (
	id INT NOT NULL PRIMARY KEY,
	Iso_Pays varchar(15) NOT NULL CONSTRAINT isopays_fk REFERENCES Pays(ISO),
	date DATE NOT NULL,
	Id_Epi INT CONSTRAINT idepi_fk REFERENCES Epidemiologiste(id),
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
