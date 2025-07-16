-- Introdução ao Armazenamento e Análise de Dados (IAAD) - BSI/UFRPE
-- Script SQL de criação e carga do banco de dados Programacao_Filmes 

BEGIN;
DROP SCHEMA IF EXISTS Programacao_Filmes;
CREATE SCHEMA Programacao_Filmes;
USE Programacao_Filmes;

-- Criando as tabelas do banco de dados Programacao_Filmes
CREATE TABLE Canal(
  num_canal INT NOT NULL, 
  nome VARCHAR(50) NOT NULL, 
  PRIMARY KEY (num_canal)
);

CREATE TABLE Filme(
  num_filme INT NOT NULL,
  nome VARCHAR(80) NOT NULL,
  ano DECIMAL(4),
  duracao INT NOT NULL,
  PRIMARY KEY (num_filme)
);

CREATE TABLE Exibicao(
  num_filme INT NOT NULL,
  num_canal INT NOT NULL,
  data DATE NOT NULL,
  hora TIME NOT NULL,
  PRIMARY KEY (num_filme, num_canal, data, hora)
);

CREATE TABLE Elenco(
  num_filme INT NOT NULL,
  nome_ator VARCHAR(100) NOT NULL,
  protagonista BOOL NOT NULL,
  PRIMARY KEY (num_filme, nome_ator)
);
	
-- Populando/carregando as tabelas do banco de dados
INSERT INTO Canal VALUES
(111, 'AXN'),
(222, 'HBO'),
(333, 'Cinemax'),
(444, 'TNT'),
(555, 'Telecine'),
(666, 'Megapix');	
INSERT INTO Filme VALUES
(90001, 'Avatar', 2022, 162),
(90002, 'Titanic', 1997, 194),
(90003, 'Star Wars', 2019),
(90004, 'Vingadores Ultimato', 2019, 180),
(90005, 'Lilo & Stitch', 2025, 108),
(90006, 'O Poderoso Chefão', 1972, 175),
(90007, 'Batman: O Cavaleiro das Trevas', 2008, 152),
(90008, 'O Senhor dos Anéis: A Sociedade do Anel', 2002, 178),
(90009, 'Clube da Luta', 1999, 139),
(90010, 'Interestelar', 2014, 169),
(90011, 'A Viagem de Chihiro', 2001, 124),
(90012, 'Psicose', 1960, 109),
(90013, 'Whiplash: Em Busca da Perfeição', 2014, 106),
(90014, 'Homem-Aranha: Através do Aranhaverso', 2023, 140),
(90015, 'Duna: Parte 2', 2024, 166),
(90016, '10 Coisas que Eu Odeio em Você', 1999, 97),
(90017, 'As Patricinhas de Beverly Hills', 1995, 97),
(90018, 'Como Perder um Homem em 10 Dias', 2003, 116),
(90019, 'Your Name', 2016, 106),
(90020, 'O Castelo Animado', 2004, 119),
(90021, 'As Branquelas', 2004, 109),
(90022, 'Oppenheimer', 2023, 180),
(90023, 'Cisne Negro', 2010, 108),
(90024, 'La La Land: Cantando Estações', 2016, 128),
(90025, 'O Show de Truman: O Show da Vida', 1998, 103);		
INSERT INTO Exibicao VALUES
(90001, 222, '2025-06-27', '14:00:00'),
(90003, 111, '2025-06-27', '19:45:00'),
(90002, 333, '2025-06-28', '09:30:00'),
(90002, 333, '2025-06-28', '20:30:00'),
(90005, 222, '2025-08-03', '16:20:00'),
(90005, 333, '2025-08-03', '16:20:00'),
(90016, 555, '2025-07-13', '21:25:00'),
(90014, 111, '2025-07-21', '10:00:00'),
(90007, 333, '2025-06-23', '21:15:00'),
(90021, 222, '2025-08-01', '13:20:00'),
(90014, 555, '2015-07-21', '19:00:00'),
(90020, 666, '2025-08-01', '13:20:00'),
(90007, 333, '2025-07-23', '21:15:00'),
(90009, 555, '2025-08-04', '22:30:00'),
(90002, 333, '2025-07-12', '14:40:00'),
(90024, 555, '2025-09-24', '16:10:00'),
(90011, 666, '2025-08-20', '17:25:00'),
(90002, 333, '2025-07-13', '02:40:00'),
(90021, 444, '2025-08-25', '15:25:00'),
(90006, 555, '2025-09-02', '03:00:00'),
(90012, 111, '2025-08-01', '17:45:00'),
(90003, 111, '2025-08-01', '20:00:00'),
(90019, 666, '2025-09-02', '02:40:00'),
(90005, 555, '2025-09-01', '10:00:00'),
(90017, 444, '2025-07-24', '21:25:00'),
(90020, 444, '2025-08-03', '15:00:00'),
(90025, 666, '2025-08-04', '15:00:00'),
(90008, 333, '2025-08-16', '16:40:00'),
(90016, 666, '2025-07-31', '20:30:00'),
(90009, 444, '2025-07-24', '22:00:00');
INSERT INTO Elenco VALUES
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
(90005, 'Maia Kealoha', 1),
(90005, 'Sydney Agudong', 0),
(90005, 'Billy Magnussen', 0)
(90006, 'Marlon Brando', 1),
(90006, 'Al Pacino', 1),
(90006, 'Diane Keaton', 0),
(90007, 'Christian Bale', 1),
(90007, 'Heath Ledger', 0),
(90007, 'Aaron Eckhart', 0),
(90008, 'Elijah Wood', 1),
(90008, 'Ian McKellen', 0),
(90008, 'Orlando Bloom', 0),
(90009, 'Edward Norton', 1),
(90009, 'Brad Pitt', 1),
(90009, 'David Andrews', 0),
(90010, 'Matthew McConaughey', 1),
(90010, 'Anne Hathaway', 0),
(90010, 'Jessica Chastain', 0),
(90011, 'Rumi Hiiragi', 1),
(90011, 'Mari Natsuki', 0),
(90011, 'Takashi Naitô', 0),
(90012, 'Anthony Perkins', 1),
(90012, 'Janet Leigh', 1),
(90012, 'Vera Miles', 0),
(90013, 'Miles Teller', 1),
(90013, 'J.K. Simmons', 0),
(90013, 'Melissa Benoist', 0),
(90014, 'Shameik Moore', 1),
(90014, 'Hailee Steinfeld', 0),
(90014, 'Oscar Isaac', 0),
(90015, 'Timothée Chalamet', 1),
(90015, 'Zendaya', 0),
(90015, 'Josh Brolin', 0),
(90016, 'Julia Stiles', 1),
(90016, 'Heath Ledger', 1),
(90016, 'Joseph Gorgon-Levitt', 0),
(90017, 'Alicia Silverstone', 1),
(90017, 'Brittany Murphy', 0),
(90017, 'Paul Rudd', 0),
(90018, 'Kate Hudson', 1),
(90018, 'Matthew McConaughey', 1),
(90018, 'Kathryn Hahn', 0),
(90019, 'Ryûnosuke Kamiki', 1),
(90019, 'Mone Kamishiraishi', 1),
(90019, 'Ryo Narita', 0),
(90020, 'Chieko Baishô', 1),
(90020, 'Takuya Kimura', 1),
(90020, 'Tatsuya Gashûin', 0),
(90021, 'Marlon Wayans', 1),
(90021, 'Shawn Wayans', 1),
(90021, 'Terry Crews', 0),
(90022, 'Cillian Murphy', 1),
(90022, 'Emily Blunt', 0),
(90022, 'Robert Downey Jr.', 0),
(90023, 'Natalie Portman', 1),
(90023, 'Vincent Cassel', 0),
(90023, 'Winona Ryder', 0),
(90024, 'Ryan Gosling', 1),
(90024, 'Emma Stone', 1),
(90024, 'J.K. Simmons', 0),
(90025, 'Jim Carrey', 1),
(90025, 'Ed Harris', 0),
(90025, 'Laura Linney', 0);

-- Aplicando a restrição de integridade referencial (chaves estrangeiras - FK)
ALTER TABLE Exibicao	ADD FOREIGN KEY(num_filme) REFERENCES Filme(num_filme);
ALTER TABLE Exibicao	ADD FOREIGN KEY(num_canal) REFERENCES Canal(num_canal);
ALTER TABLE Elenco	ADD FOREIGN KEY(num_filme) REFERENCES Filme(num_filme);

COMMIT;
