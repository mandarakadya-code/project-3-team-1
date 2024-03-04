CREATE TABLE IF NOT EXISTS public.annual_emission
(
    "Entity" character varying(255) COLLATE pg_catalog."default",
    "Code" character varying(25) COLLATE pg_catalog."default",
    "year_" bigint,
    annual_co2_emissions float
	
)
CREATE TABLE IF NOT EXISTS public.per_capita_emissions
(
    "Entity" character varying(255) COLLATE pg_catalog."default",
    "Code" character varying(25) COLLATE pg_catalog."default",
    "year_" bigint,
    annual_co2_emissions float
	
)


select * 
from annual_emission


select * 
from per_capita_emissions