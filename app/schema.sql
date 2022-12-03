CREATE TABLE IF NOT EXISTS recordD (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  popis TEXT NOT NULL,
  jazyk TEXT NOT NULL,
  hodnoceni INTEGER NOT NULL
);
insert into recordD (name, popis, jazyk, hodnoceni) values ('Dan', 'Ano', 'C++', 5);
insert into recordD (name, popis, jazyk, hodnoceni) values ('Idiot', 'Ano', 'php', 1);
insert into recordD (name, popis, jazyk, hodnoceni) values ('Dan', 'Ne', 'C++', 5);