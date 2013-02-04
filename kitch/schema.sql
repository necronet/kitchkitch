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
password varchar(64) not null, #SHA1 base passwords
pincode	char(4) default '0000',#Default pincode for accesing
active int default 1,
unique(username) );

#Hold data regarding data to be use in the user encryption schemas
drop table if exists meta_users;
create table meta_users (
  user_uid varchar(36) primary key,
  iteraction int not null,
  product varchar(36),
  modified_on int not null
);

insert into users values('c4860202-6e59-11e2-b8ac-3c0754558970','admin','d82670cb1512cddcf3a5b0d0760f65cf5a67704951abb3d45180e87eb31e5e6f',6969,1);
insert into meta_users values('c4860202-6e59-11e2-b8ac-3c0754558970',50000,'98e8eb4f-6e59-11e2-b9a9-3c0754558970',1359934187);

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

insert into menus values('702ef8f0-6a5b-11e2-9d54-3c075455897','Menu Test',1);

drop table if exists items;
create table items (
 uid varchar(36) primary key,
 title varchar(100) not null, #Dishes longer thatn 100 character really?
 description varchar(1000) not null,#1000 character should be good enough to describe a dish
 price decimal(6,2) not null,
 active int default 1
);

insert into items values('102ef8f0-6a5b-11e2-9d54-3c075455897','Menu Item Test','This is just a test',500,1);
insert into items values('202ef8f0-6a5b-11e2-9d54-3c075455897','Menu Item ','Second test',101,1);
insert into items values('302ef8f0-6a5b-11e2-9d54-3c075455897','Iem of Menu','This is just a test',120,1);

drop table if exists menus_items;
create table menus_items (
 menus_uid varchar(36),
 items_uid varchar(36),
 active int default 1,
 primary key(menus_uid,items_uid)
);

insert into menus_items values('702ef8f0-6a5b-11e2-9d54-3c075455897','102ef8f0-6a5b-11e2-9d54-3c075455897',1);
insert into menus_items values('702ef8f0-6a5b-11e2-9d54-3c075455897','202ef8f0-6a5b-11e2-9d54-3c075455897',1);
insert into menus_items values('702ef8f0-6a5b-11e2-9d54-3c075455897','302ef8f0-6a5b-11e2-9d54-3c075455897',1);
