CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
do $$ 
declare
   uuid_epi uuid := uuid_generate_v4();
begin 
   INSERT INTO epidemiologiste(uuid) VALUES (uuid_epi);
   UPDATE utilisateur SET pseudo='Sacha', mot_de_passe='pbkdf2_sha256$216000$NRinKHRX2HRS$cTc6kK/J9gBDSSCrfMCOkPObJZMwCD+dX4jpLrNtqfM=' WHERE uuid=uuid_epi; -- mdp Pikachu
   INSERT INTO utilisateur(uuid, pseudo, mot_de_passe) VALUES (uuid_generate_v4(), 'Mexico', 'pbkdf2_sha256$216000$pCVu3XDSZheC$NEinlyMbhKgiRMsYh9XervDSj/k56a4Qyasa6Os1SvI='); --mdp Sombrero
end $$;
