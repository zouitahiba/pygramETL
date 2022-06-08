begin;

-- schema
drop schema if exists "SecuriteRoutiere" cascade;
create schema "SecuriteRoutiere";
set search_path to "SecuriteRoutiere";

create table TempsDebutEv(
   id_TempsD varchar,
   moisTempsD int,
   anneeTempsD int
);
create table LocationA(
   id_Location varchar,
   Rue varchar,
   Codemunicipal varchar
);
create table Evenement(
   id_Evenement varchar,
   nombrePersonneEv int
);

-- table Fait
create table Accident(
   montantDommage float,
   id_TempsD varchar,
   id_Location varchar, 
   id_Evenement varchar
);

-- primary keys
alter table TempsDebutEv add primary key(id_TempsD);
alter table LocationA add primary key(id_Location);
alter table Evenement add primary key(id_Evenement);
alter table Accident add primary key(id_TempsD, id_Location, id_Evenement);


-- foreign keys
alter table Accident add foreign key(id_TempsD) references TempsDebutEv, add foreign key(id_Location) references LocationA, add foreign key(id_Evenement) references Evenement;
  


commit;