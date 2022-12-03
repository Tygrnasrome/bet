CREATE TABLE IF NOT EXISTS name (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     name VARCHAR NOT NULL
);
insert into name (name) values ('Robert');
insert into name (name) values ('Pavel');
insert into name (name) values ('Ondra');

CREATE TABLE IF NOT EXISTS jazyk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL
);
insert into jazyk (name) values ('php');
insert into jazyk (name) values ('holyC');
insert into jazyk (name) values ('C++';

CREATE TABLE IF NOT EXISTS record (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name_id INTEGER NOT NULL,
  popis VARCHAR NOT NULL,
  jazyk_id INTEGER NOT NULL,
  hodnoceni INTEGER NOT NULL
);
insert into record (name_id, popis, jazyk_id, hodnoceni) values (1, 'Ano', 1, 5);
insert into record (name_id, popis, jazyk_id, hodnoceni) values (2, 'Ano', 2, 1);
insert into record (name_id, popis, jazyk_id, hodnoceni) values (3, 'Ne', 3, 5);
