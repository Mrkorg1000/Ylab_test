ALTER USER postgres WITH ENCRYPTED PASSWORD 'postgres';
CREATE DATABASE menu_db;
GRANT ALL PRIVILIGES ON DATABASE menu_db TO postgres;