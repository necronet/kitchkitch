drop table if exist users;
create table users( user_id string primary key, 
username string not null, 
password string not null,
active int default 0);

drop table if exists menus;
create table menus (
  id integer primary key autoincrement,
  title string not null
);
