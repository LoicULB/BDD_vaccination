CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
do $$ 
declare
   uuid_epi uuid := uuid_generate_v4();
begin 
   INSERT INTO epidemiologiste(uuid) VALUES (uuid_epi);
   UPDATE utilisateur SET pseudo='Sacha', mot_de_passe='Pikachu' WHERE uuid=uuid_epi;
   INSERT INTO utilisateur(uuid, pseudo, mot_de_passe) VALUES (uuid_generate_v4(), 'Mexico', 'Sombrero');
end $$;
