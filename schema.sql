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
