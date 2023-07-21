create database inventory_management;
use inventory_management;
create table product (
product_id varchar(50) not null,
primary key (product_id)
);
create table location(
location_id varchar(50) not null,
primary key (location_id)
);
create table productManagement(
from_location varchar(50),
to_location varchar(50),
product_id varchar(50) not null,
qty int not null
);

create table report(
location_id varchar(50) not null ,
product_id varchar(50) not null,
qty int not null
);


