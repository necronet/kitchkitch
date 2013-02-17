/*
* 	Users and privileges configuration
*/

GRANT USAGE ON *.* TO 'kitch'@'localhost';
DROP USER 'kitch'@'localhost';
FLUSH PRIVILEGES;

#Users should only have permission to select, insert or update. 
##To prevent deletion or alteration of any sort in the database.
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

#unadmin is a test user for testing resources permissions
insert into users values('a4860202-6e59-11e2-b8ac-3c0754558970','unadmin','d82670cb1512cddcf3a5b0d0760f65cf5a67704951abb3d45180e87eb31e5e6f',6969,1);
insert into meta_users values('a4860202-6e59-11e2-b8ac-3c0754558970',50000,'98e8eb4f-6e59-11e2-b9a9-3c0754558970',1359934187);


#Tokens are needed for validate the authenticity of a user, instead of passing username, password everytime.
#the app should pass a validated token
drop table if exists tokens;
create table tokens( 
user_uid varchar(36) not null,
token varchar(40) not null,
active int default 1,
primary key(user_uid,token));

#Group will hold general membership to which users can be. This will be highly tied with the 
#permission that a user amy have over a specific Resource and specific condition in which they
#might be able to execute it.
drop table if exists groups;
create table groups( 
uid varchar(36) not null primary key,
name varchar(40) not null unique,
active int default 1);

#Default group for administrative 
insert into groups(uid,name) values('64344887-7902-11e2-821d-3c0754558970','Administrator');


#Map a user with multiples groups this is useful to get the permission
drop table if exists users_groups;
create table users_groups( 
group_uid varchar(36) not null ,
user_uid varchar(36) not null,
primary key (group_uid, user_uid));

#admin to administrative users
insert into users_groups values('64344887-7902-11e2-821d-3c0754558970','c4860202-6e59-11e2-b8ac-3c0754558970');

#List of available permission might contain 
drop table if exists permissions;
create table permissions(
uid varchar(36) not null primary key,
name varchar(40) not null unique,
active int default 1);

insert into permissions(uid,name) values ('158d527d-7901-11e2-bc99-3c0754558970','put'),
										 ('258d527d-7901-11e2-bc99-3c0754558970','post'),
										 ('358d527d-7901-11e2-bc99-3c0754558970','get'),
										 ('458d527d-7901-11e2-bc99-3c0754558970','delete');

#List of available resources in the system login, menus, menusItems, user, etc....
drop table if exists resources;
create table resources(
uid varchar(36) not null primary key,
name varchar(40) not null unique,
active int default 1);

insert into resources(uid,name) values('00160202-6e59-11e2-b8ac-3c0754558970','user');
insert into resources(uid,name) values('00260202-6e59-11e2-b8ac-3c0754558970','login');
insert into resources(uid,name) values('00360202-6e59-11e2-b8ac-3c0754558970','menus');
insert into resources(uid,name) values('00460202-6e59-11e2-b8ac-3c0754558970','menuItems');

#Table that map a group, resources and the permission this can have
drop table if exists group_resources_permission;
create table group_resources_permission(
	group_uid varchar(36) not null,
	resource_uid varchar(36) not null,
	permission_uid varchar(36) not null,
	primary key(group_uid, resource_uid, permission_uid)
);

#Set Admin group to post put delete for user resources
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00160202-6e59-11e2-b8ac-3c0754558970','158d527d-7901-11e2-bc99-3c0754558970');
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00160202-6e59-11e2-b8ac-3c0754558970','258d527d-7901-11e2-bc99-3c0754558970');
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00160202-6e59-11e2-b8ac-3c0754558970','358d527d-7901-11e2-bc99-3c0754558970');
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00160202-6e59-11e2-b8ac-3c0754558970','458d527d-7901-11e2-bc99-3c0754558970');

#Set Admin group to post put delete for menus resources
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00360202-6e59-11e2-b8ac-3c0754558970','158d527d-7901-11e2-bc99-3c0754558970');
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00360202-6e59-11e2-b8ac-3c0754558970','258d527d-7901-11e2-bc99-3c0754558970');
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00360202-6e59-11e2-b8ac-3c0754558970','358d527d-7901-11e2-bc99-3c0754558970');
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00360202-6e59-11e2-b8ac-3c0754558970','458d527d-7901-11e2-bc99-3c0754558970');

#Set Admin group to post put delete for menusItems resources
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00460202-6e59-11e2-b8ac-3c0754558970','158d527d-7901-11e2-bc99-3c0754558970');
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00460202-6e59-11e2-b8ac-3c0754558970','258d527d-7901-11e2-bc99-3c0754558970');
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00460202-6e59-11e2-b8ac-3c0754558970','358d527d-7901-11e2-bc99-3c0754558970');
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00460202-6e59-11e2-b8ac-3c0754558970','458d527d-7901-11e2-bc99-3c0754558970');

#Menus modules
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
