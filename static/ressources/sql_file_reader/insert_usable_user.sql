CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
do $$ 
declare
   uuid_epi uuid := uuid_generate_v4();
begin 
   INSERT INTO epidemiologiste(uuid) VALUES (uuid_epi);
   UPDATE utilisateur SET pseudo='Sacha', mot_de_passe='pbkdf2_sha256$216000$NRinKHRX2HRS$cTc6kK/J9gBDSSCrfMCOkPObJZMwCD+dX4jpLrNtqfM=' WHERE uuid=uuid_epi; -- mdp Pikachu
   INSERT INTO utilisateur(uuid, pseudo, mot_de_passe) VALUES (uuid_generate_v4(), 'Mexico', 'pbkdf2_sha256$216000$pCVu3XDSZheC$NEinlyMbhKgiRMsYh9XervDSj/k56a4Qyasa6Os1SvI='); --mdp Sombrero
end $$;
UPDATE utilisateur SET rue_adresse='Rue Infection', code_postal_adresse='1040', numero_adresse='108', ville_adresse='Ghost City' WHERE pseudo='Sacha';
UPDATE utilisateur SET rue_adresse='Rue Perlimpinpin', code_postal_adresse='1050', numero_adresse='120', ville_adresse='Harem City' WHERE pseudo='Mexico';
UPDATE epidemiologiste SET centre='Pokemon' , telephone_service=$$0471/78/12/17$$ WHERE uuid =(SELECT uuid FROM utilisateur WHERE pseudo='Sacha');

--for test integrity INSERT INTO utilisateur(uuid, pseudo, mot_de_passe, numero_adresse, ville_adresse, code_postal_adresse, rue_adresse) VALUES (uuid_generate_v4(), 'Tot', 'testo', 123, 'Jambono', 1040, 'Ghost city'); --mdp Sombrero