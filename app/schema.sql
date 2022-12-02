CREATE TABLE IF NOT EXISTS record (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  descr TEXT NOT NULL,
  jazyk TEXT NOT NULL,
  hodnoceni INT NOT NULL
);
insert into record (name, descr, jazyk, hodnoceni) values ('Dan', 'Ano', 'C++', 5);
insert into record (name, descr, jazyk, hodnoceni) values ('Dan', 'Ano', 'C++', 5);
insert into record (name, descr, jazyk, hodnoceni) values ('Dan', 'Ano', 'C++', 5);