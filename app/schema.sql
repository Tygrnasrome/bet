CREATE TABLE IF NOT EXISTS record (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  popis TEXT NOT NULL,
  jazyk TEXT NOT NULL,
  hodnoceni INT NOT NULL
);
insert into record (name, popis, jazyk, hodnoceni) values ('Dan', 'Ano', 'C++', 5);
insert into record (name, popis, jazyk, hodnoceni) values ('Idiot', 'Ano', 'php', 1);
insert into record (name, popis, jazyk, hodnoceni) values ('Dan', 'Ne', 'C++', 5);