/*
This script will create the schema and defaults values of kitch API.
Considere to add

Fee free to edit this script as you like
*/

drop table if exists users;
create table users( 
uid string primary key, 
username string not null, 
password string not null,
active int default 1);

insert into users values('21232f297a57a5a743894a0e4a801fc3','admin','admin',1);

drop table if exists tokens;
create table tokens( 
uid string not null, 
token string not null,
active int default 1,
primary key(uid,token));


drop table if exists menus;
create table menus (
 uid string primary key,
 title string not null,
 active int default 1
);

drop table if exists items;
create table items (
 uid string primary key,
 title string not null,
 description string not null,
 price real not null,
 active int default 1
);

drop table if exists menus_items;
create table menus_items (
 menus_uid string,
 items_uid string,
 primary key(menus_uid,items_uid)
);