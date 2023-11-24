CREATE USER midas_sales WITH PASSWORD 'amScD6paIx9EcKT3jeBw';

CREATE DATABASE midas_sales;

ALTER DATABASE midas_sales owner to midas_sales;

GRANT ALL PRIVILEGES ON DATABASE midas_sales TO midas_sales;

grant create on schema public to public;

