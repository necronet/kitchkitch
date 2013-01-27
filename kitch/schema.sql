/*
* 	Users and privileges configuration
*/

GRANT USAGE ON *.* TO 'kitch'@'localhost';
DROP USER 'kitch'@'localhost';
FLUSH PRIVILEGES;

create user 'kitch'@'localhost' identified by 'kitch';
grant select, insert, update on kitch.* to 'kitch'@'localhost';
grant select, insert, update on kitch_test.* to 'kitch'@'localhost';

flush privileges;

/*
This script will create the schema and defaults values of kitch API.
Considere to add

Fee free to edit this script as you like
*/

drop table if exists users;
create table users( 
uid varchar(36) primary key, 
username varchar(50) not null, #Username bigger than 50? I don't think so
password varchar(40) not null, #SHA1 base passwords
pincode	int default 6969,
active int default 1);

insert into users values('21232f297a57a5a743894a0e4a801fc3','admin','admin',6969,1);

drop table if exists tokens;
create table tokens( 
uid varchar(36) not null, 
token varchar(40) not null,
active int default 1,
primary key(uid,token));


drop table if exists menus;
create table menus (
 uid varchar(36) primary key,
 title varchar(100) not null, #Menus title bigger than 100 character don't expect to see this
 active int default 1
);

drop table if exists items;
create table items (
 uid varchar(36) primary key,
 title varchar(100) not null, #Dishes longer thatn 100 character really?
 description varchar(1000) not null,#1000 character should be good enough to describe a dish
 price decimal(6,2) not null,
 active int default 1
);

drop table if exists menus_items;
create table menus_items (
 menus_uid varchar(36),
 items_uid varchar(36),
 active int default 1,
 primary key(menus_uid,items_uid)
);