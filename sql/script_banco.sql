BEGIN;

DROP SCHEMA IF EXISTS Programacao_Filmes;

CREATE SCHEMA Programacao_Filmes;

USE Programacao_Filmes;

CREATE TABLE Canal (
  num_canal INT NOT NULL,
  nome VARCHAR(50) NOT NULL,
  PRIMARY KEY (num_canal)
);

CREATE TABLE Filme (
  num_filme INT NOT NULL,
  nome VARCHAR(80) NOT NULL,
  ano DECIMAL(4),
  duracao INT,
  PRIMARY KEY (num_filme)
);

CREATE TABLE Exibicao (
  num_filme INT NOT NULL,
  num_canal INT NOT NULL,
  data DATE NOT NULL,
  hora TIME NOT NULL, 
  PRIMARY KEY (num_filme, num_canal, data, hora)
);

CREATE TABLE Elenco (
  num_filme INT NOT NULL,
  nome_ator VARCHAR(100) NOT NULL, 
  protagonista BOOL NOT NULL,
  PRIMARY KEY (num_filme, nome_ator)
);


INSERT INTO Canal VALUES
(111, 'AXN'),
(222, 'HBO'),
(333, 'Cinemax'),
(444, 'TNT');

INSERT INTO Filme VALUES
(90001, 'Avatar', 2022, 162),
(90002, 'Titanic', 1997, 194),
(90003, 'Star Wars', 2019, NULL), -- Inserindo NULL explicitamente
(90004, 'Vingadores Ultimato', 2019, 180),
(90005, 'Lilo & Stitch', 2025, 108);

INSERT INTO Exibicao VALUES
(90001, 222, '2025-06-27', '14:00:00'),
(90003, 111, '2025-06-27', '19:45:00'),
(90002, 333, '2025-06-28', '09:30:00'),
(90002, 333, '2025-06-28', '20:30:00'),
(90005, 222, '2025-08-03', '16:20:00'),
(90005, 333, '2025-08-03', '16:20:00');

INSERT INTO Elenco VALUES
-- Adicionadas as vírgulas que faltavam
(90001, 'Sam Worthington', 1),
(90001, 'Zoë Saldaña', 1),
(90001, 'Sigourney Weaver', 0),
(90002, 'Kate Winslet', 1),
(90002, 'Leonardo DiCaprio', 1),
(90002, 'Billy Zane', 0),
(90003, 'Daisy Ridley', 1),
(90003, 'Mark Hamill', 0),
(90003, 'Harrison Ford', 0),
(90004, 'Robert Downey Jr.', 1),
(90004, 'Josh Brolin', 0),
(90004, 'Zoë Saldaña', 0),
(90004, 'Billy Magnussen', 0),
(90005, 'Maia Kealoha', 1),
(90005, 'Sydney Agudong', 0);

ALTER TABLE Exibicao
  ADD FOREIGN KEY (num_filme) REFERENCES Filme (num_filme);

ALTER TABLE Exibicao
  ADD FOREIGN KEY (num_canal) REFERENCES Canal (num_canal);

ALTER TABLE Elenco
  ADD FOREIGN KEY (num_filme) REFERENCES Filme (num_filme);

COMMIT;