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
drop table if exists users_groups;
drop table if exists group_resources_permission;
drop table if exists meta_users;
drop table if exists tokens;
drop table if exists users;
drop table if exists groups;


create table users( 
uid varchar(36) primary key, 
username varchar(50) not null, #Username bigger than 50? I don't think so
password varchar(64) not null, #SHA1 base passwords
pincode	char(4) default '0000',#Default pincode for accesing
active int default 1,
unique(username) ) ENGINE=InnoDB;

#Hold data regarding data to be use in the user encryption schemas

create table meta_users (
  user_uid varchar(36) primary key,
  iteraction int not null,
  product varchar(36),
  modified_on int not null,
  foreign key (user_uid) references users(uid)
) ENGINE=InnoDB;

insert into users values('c4860202-6e59-11e2-b8ac-3c0754558970','admin','d82670cb1512cddcf3a5b0d0760f65cf5a67704951abb3d45180e87eb31e5e6f',6969,1);
insert into meta_users values('c4860202-6e59-11e2-b8ac-3c0754558970',50000,'98e8eb4f-6e59-11e2-b9a9-3c0754558970',1359934187);

#unadmin is a test user for testing resources permissions
insert into users values('a4860202-6e59-11e2-b8ac-3c0754558970','unadmin','d82670cb1512cddcf3a5b0d0760f65cf5a67704951abb3d45180e87eb31e5e6f',6969,1);
insert into meta_users values('a4860202-6e59-11e2-b8ac-3c0754558970',50000,'98e8eb4f-6e59-11e2-b9a9-3c0754558970',1359934187);


#Tokens are needed for validate the authenticity of a user, instead of passing username, password everytime.
#the app should pass a validated token

create table tokens( 
user_uid varchar(36) not null,
token varchar(40) not null,
active int default 1,
primary key(user_uid,token),
foreign key (user_uid) references users(uid)) ENGINE=InnoDB;

#Group will hold general membership to which users can be. This will be highly tied with the 
#permission that a user amy have over a specific Resource and specific condition in which they
#might be able to execute it.
create table groups( 
uid varchar(36) not null primary key,
name varchar(50) not null unique,
active int default 1) ENGINE=InnoDB;

#Default group for administrative 
insert into groups(uid,name) values('64344887-7902-11e2-821d-3c0754558970','Administrator');


#Map a user with multiples groups this is useful to get the permission
create table users_groups( 
group_uid varchar(36) not null ,
user_uid varchar(36) not null,
primary key (group_uid, user_uid),
foreign key (user_uid) references users(uid),
foreign key (group_uid) references groups(uid)) ENGINE=InnoDB;

#admin to administrative users
insert into users_groups values('64344887-7902-11e2-821d-3c0754558970','c4860202-6e59-11e2-b8ac-3c0754558970');

#List of available permission might contain 
drop table if exists permissions;
create table permissions(
uid varchar(36) not null primary key,
name varchar(40) not null unique,
active int default 1) ENGINE=InnoDB;

insert into permissions(uid,name) values ('158d527d-7901-11e2-bc99-3c0754558970','put'),
										 ('258d527d-7901-11e2-bc99-3c0754558970','post'),
										 ('358d527d-7901-11e2-bc99-3c0754558970','get'),
										 ('458d527d-7901-11e2-bc99-3c0754558970','delete');

#List of available resources in the system login, menus, menusItems, user, etc....
drop table if exists resources;
create table resources(
uid varchar(36) not null primary key,
name varchar(40) not null unique,
active int default 1) ENGINE=InnoDB;

insert into resources(uid,name) values('00160202-6e59-11e2-b8ac-3c0754558970','user');
insert into resources(uid,name) values('00260202-6e59-11e2-b8ac-3c0754558970','login');
insert into resources(uid,name) values('00360202-6e59-11e2-b8ac-3c0754558970','menus');
insert into resources(uid,name) values('00460202-6e59-11e2-b8ac-3c0754558970','menuItems');
insert into resources(uid,name) values('00560202-6e59-11e2-b8ac-3c0754558970','table');

#Table that map a group, resources and the permission this can have
create table group_resources_permission(
	group_uid varchar(36) not null,
	resource_uid varchar(36) not null,
	permission_uid varchar(36) not null,
	primary key(group_uid, resource_uid, permission_uid),
	foreign key (group_uid) references groups(uid),
	foreign key (resource_uid) references resources(uid),
	foreign key (permission_uid) references permissions(uid)
) ENGINE=InnoDB;

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

#Set Admin group to post put delete for tables resources
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00560202-6e59-11e2-b8ac-3c0754558970','158d527d-7901-11e2-bc99-3c0754558970');
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00560202-6e59-11e2-b8ac-3c0754558970','258d527d-7901-11e2-bc99-3c0754558970');
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00560202-6e59-11e2-b8ac-3c0754558970','358d527d-7901-11e2-bc99-3c0754558970');
insert into group_resources_permission values('64344887-7902-11e2-821d-3c0754558970','00560202-6e59-11e2-b8ac-3c0754558970','458d527d-7901-11e2-bc99-3c0754558970');

#Menus modules
drop table if exists menus;
create table menus (
 uid varchar(36) primary key,
 title varchar(100) not null, #Menus title bigger than 100 character don't expect to see this
 active int default 1
) ENGINE=InnoDB;

insert into menus values('702ef8f0-6a5b-11e2-9d54-3c075455897','Menu Test',1);

drop table if exists items;
create table items (
 uid varchar(36) primary key,
 title varchar(100) not null, #Dishes longer thatn 100 character really?
 description varchar(1000) not null,#1000 character should be good enough to describe a dish
 price decimal(6,2) not null,
 active int default 1,
 addon int default 0 #Describe wether this specific item is an addon or not
) ENGINE=InnoDB;

insert into items(uid,title,description,price) values('102ef8f0-6a5b-11e2-9d54-3c075455897','Menu Item Test','This is just a test',500);
insert into items(uid,title,description,price) values('202ef8f0-6a5b-11e2-9d54-3c075455897','Menu Item ','Second test',101);
insert into items(uid,title,description,price) values('302ef8f0-6a5b-11e2-9d54-3c075455897','Iem of Menu','This is just a test',120);

drop table if exists menus_items;
create table menus_items (
 menus_uid varchar(36),
 items_uid varchar(36),
 active int default 1,
 primary key(menus_uid,items_uid)
) ENGINE=InnoDB;

insert into menus_items values('702ef8f0-6a5b-11e2-9d54-3c075455897','102ef8f0-6a5b-11e2-9d54-3c075455897',1);
insert into menus_items values('702ef8f0-6a5b-11e2-9d54-3c075455897','202ef8f0-6a5b-11e2-9d54-3c075455897',1);
insert into menus_items values('702ef8f0-6a5b-11e2-9d54-3c075455897','302ef8f0-6a5b-11e2-9d54-3c075455897',1);


drop table if exists tables;
create table tables (
 uid varchar(36) primary key,
 name varchar(100) not null unique, #It could be numeric or could be by other name
 active int default 1
) ENGINE=InnoDB;

#Represent an order 
drop table if exists orders;
create table orders (
 uid varchar(36) primary key,
 name varchar(100) , #This will identify the order, in the app this might be autogerated.
 started_on timestamp not null
) ENGINE=InnoDB;

#Holds the tables for a specific order.
drop table if exists orders_tables;
create table orders_tables (
 table_uid varchar(36) not null,
 order_uid varchar(36) not null
) ENGINE=InnoDB;


drop table if exists orders_details;
create table orders_details(
	uid varchar(36) not null primary key,
	order_uid varchar(36) not null,
	item_uid varchar(36) not null,
	menu_uid varchar(36) not null,
	item_description varchar(100) not null,
	price decimal(6,2) not null,
	quantity int 
) ENGINE=InnoDB;

#Holds the records of the states of the orders this table will be non modifiable 
#makes no sense to modify this records.
drop table if exists orders_details_states;
create table orders_details_states( 
 order_detail_uid varchar(36) not null,
 state_id int not null,
 created_on timestamp not null,
 primary key(order_detail_uid, state_id)
) ENGINE=InnoDB;

#Represent general states in the application 
drop table if exists states;
create table states(
	id int not null  auto_increment primary key,
	name varchar(30) not null
) ENGINE=InnoDB;

insert into states(name) values('Ordered');
insert into states(name) values('Ready');
insert into states(name) values('Served');
insert into states(name) values('Cleaned');