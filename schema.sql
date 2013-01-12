drop table if exists users;
create table users( user_id string primary key, 
username string not null, 
password string not null,
active int default 0);

insert into users values('21232f297a57a5a743894a0e4a801fc3','admin','admin',1);

drop table if exists menus;
create table menus (
  id integer primary key autoincrement,
  title string not null
);
