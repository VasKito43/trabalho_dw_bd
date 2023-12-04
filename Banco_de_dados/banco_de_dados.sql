drop table if EXISTS cliente CASCADE;
drop table if EXISTS funcionario CASCADE;
drop table if EXISTS onibus CASCADE;
drop table if EXISTS viagem CASCADE;
drop table if EXISTS cidade CASCADE;
drop table if EXISTS motorista CASCADE;
drop table if EXISTS bilhete CASCADE;
drop table if EXISTS empresa CASCADE;


CREATE table cidade(
  nome varchar(50) NOT NULL,
  estado varchar(20) NOT NULL,
  ccodigo int NOT NULL PRIMARY KEY
);

CREATE TABLE empresa(
  cnpj varchar(30) NOT NULL PRIMARY KEY,
  nome varchar(50),
  cidade int NOT NULL,
  FOREIGN KEY (cidade) REFERENCES cidade(ccodigo)
);

CREATE table cliente(
  pnome varchar(50) not NULL,
  unome varchar(50) NOT NULL,
  rg varchar(20) NOT NULL PRIMARY KEY,
  cpf varchar(20) NOT NULL,
  datanasc date,
  telefone varchar(20) NOT NULL
);

CREATE table funcionario(
  fcodigo varchar(10) PRIMARY KEY,
  senha varchar(10),
  pnome varchar(50),
  unome varchar(50),
  rg varchar(20) NOT NULL,
  cpf varchar(20) NOT NULl,
  empresa varchar(30) NOT NULL,
  cidade int NOT NULL,
  FOREIGN KEY (empresa) REFERENCES empresa(cnpj),
  FOREIGN KEY (cidade)  REFERENCES cidade(ccodigo)
);
               
CREATE TABLE onibus(
  nonibus int not NULL PRIMARY KEY,
  placa int not NULL,
  empresa varchar(30) NOT NULL,
  modelo varchar(20),
  ano int not NULL,
  classe varchar(15),
  FOREIGN KEY (empresa) REFERENCES empresa(cnpj)
);

CREATE TABLE viagem(
  cviagem int NOT NULL PRIMARY key,
  nonibus int NOT NULL,
  data date,
  horario varchar(5),
  origem int NOT NULL,
  destino int NOT NULL,
  preco int not NULL,
  FOREIGN KEY (origem) REFERENCES cidade(ccodigo),
  FOREIGN KEY (destino) REFERENCES cidade(ccodigo),
  FOREIGN key (nonibus) REFERENCES onibus(nonibus)
);
               
CREATE TABLE motorista(
  pnome varchar(50),
  unome varchar(50),
  rg varchar(20) NOT NULL,
  cpf varchar(20) NOT NULl PRIMARY KEY,
  nmotorista int not NULL,
  cviagem int NOT NULL,
  FOREIGN KEY (cviagem) REFERENCES viagem(cviagem)
);
CREATE TABLE bilhete(
  nbilhete int NOT NULL PRIMARY KEY,
  rgcliente varchar(20) NOT NULL,
  datavenda date,
  cviagem int NOT NULL,
  vendedor varchar(10) NOT NULL,
  FOREIGN key (vendedor) REFERENCES funcionario(fcodigo),
  FOREIGN key (rgcliente) REFERENCES cliente(rg),
  FOREIGN KEY (cviagem) REFERENCES viagem(cviagem)
);

INSERT INTO cidade VALUES
  ('Campo Mourão', 'Paraná', 113),
  ('Maringa', 'Paraná', 15),
  ('Londrina', 'Paraná', 1),
  ('Curitiba', 'Paraná', 99),
  ('Foz do Iguaçu', 'Paraná', 569),
  ('São Paulo', 'São Paulo', 324),
  ('Campinas', 'São Paulo', 323),
  ('Ribeirão Preto', 'São Paulo', 314),
  ('Balneário Camburiú', 'Santa Catarina', 575),
  ('Florianóplois', 'Santa Catarina', 75),
  ('Rio de Janeiro', 'Rio de Janeiro', 2),
  ('Belo Horizonte', 'Minas Gerais', 3),
  ('Brasília', 'Distrito Federal', 43),
  ('Salvador', 'Bahia', 56),
  ('Rio Branco', 'Acre', 102),
  ('Maceió', 'Alagoas', 60),
  ('Macapá', 'Amapá', 38),
  ('Manaus', 'Amazonas', 4),
  ('Fortaleza', 'Ceará', 6),
  ('Vitória', 'Espírito Santo', 8),
  ('Goiânia', 'Goiás', 9),
  ('São Luís', 'Maranhão', 10),
  ('Cuiabá', 'Mato Grosso', 11),
  ('Campo Grande', 'Mato Grosso do Sul', 12),
  ('Belém', 'Pará', 14),
  ('João Pessoa', 'Paraíba', 151),
  ('Recife', 'Pernambuco', 17),
  ('Teresina', 'Piauí', 18),
  ('Rio de Janeiro', 'Rio de Janeiro', 19),
  ('Natal', 'Rio Grande do Norte', 20),
  ('Porto Alegre', 'Rio Grande do Sul', 21),
  ('Porto Velho', 'Rondônia', 22),
  ('Boa Vista', 'Roraima', 23),
  ('Aracaju', 'Sergipe', 26),
  ('Palmas', 'Tocantins', 27);


  
INSERT into empresa VALUES
  ('111222333444', 'Brasil Sul', 1),
  ('111333444555', 'Garcia', 1),
  ('111444555666','Schimitxhi',1);

INSERT into cliente VALUES
  ('joão', 'Ferreira', '111111', '12345678999', '2000-03-23', '998754278'),
  ('Ana', 'Silva', '222222', '98765432100', '1995-05-10', '998754321'),
  ('Pedro', 'Santos', '333333', '55555555500', '1988-12-15', '998765432'),
  ('Maria', 'Oliveira', '444444', '11111111100', '2002-08-20', '998765432'),
  ('Carlos', 'Mendes', '555555', '77777777700', '1990-09-05', '998761234'),
  ('Aline', 'Pereira', '666666', '88888888800', '1985-04-14', '998762345'),
  ('Rafael', 'Fernandes', '777777', '99999999900', '1998-07-22', '998763456'),
  ('Fernanda', 'Lima', '888888', '11122233300', '2001-03-30', '998764567'),
  ('Lucas', 'Rodrigues', '999999', '44455566600', '1993-11-17', '998765678'),
  ('Isabela', 'Gomes', '101010', '77788899900', '2004-12-09', '998766789'),
  ('Bruno', 'Ferreira', '121212', '11144455500', '1996-06-28', '998767890'),
  ('Camila', 'Santana', '131313', '55577788800', '1987-01-12', '998768901'),
  ('Ricardo', 'Oliveira', '141414', '99900011100', '2000-10-03', '998769012'),
  ('Mariana', 'Pereira', '151515', '11133344400', '1992-04-18', '998770123'),
  ('Roberto', 'Santos', '161616', '66677788800', '1997-09-27', '998771234'),
  ('Felipe', 'Martins', '171717', '88899900000', '1994-08-14', '998772345'),
  ('Thiago', 'Alves', '181818', '11144455566', '1999-05-25', '998773456'),
  ('Luana', 'Sousa', '191919', '77788899911', '1991-12-02', '998774567'),
  ('Felipe', 'Melo', '202020', '55566677788', '2003-03-11', '998775678'),
  ('Juliana', 'Rocha', '212121', '99911122233', '1986-06-21', '998776789');

INSERT inTO funcionario VALUES
  ('func001', 'senha001', 'João', 'Silva', '116511', '12345678900', '111222333444', 113),
  ('func002', 'senha002', 'Maria', 'Santos', '222223', '98765432100', '111222333444', 1),
  ('func003', 'senha003', 'Pedro', 'Oliveira', '333993', '55555555500', '111222333444', 1),
  ('func004', 'senha004', 'Ana', 'Ferreira', '414444', '11111111100', '111222333444', 323),
  ('func005', 'senha005', 'Ricardo', 'Gomes', '565555', '77777777700', '111222333444', 324),
  ('func006', 'senha006', 'Camila', 'Rodrigues', '666777', '88888888800', '111333444555', 575),
  ('func007', 'senha007', 'Lucas', 'Fernandes', '127777', '99999999900', '111333444555', 75),
  ('func008', 'senha008', 'Isabela', 'Lima', '123888', '11122233300', '111333444555', 314),
  ('func009', 'senha009', 'Thiago', 'Martins', '991099', '44455566600', '111333444555', 99),
  ('func010', 'senha010', 'Aline', 'Sousa', '101011', '77788899911',  '111333444555', 15),
  ('func011', 'senha011', 'Gabriel', 'Vasco', '432156', '22233344455', '111444555666', 113);

INSERT inTO onibus VALUES
  (86226, 1234, '111333444555', 'G7', 2020, 'Leito'),
  (88009, 5678, '111333444555', 'G8', 2022, 'Semi-Leito'),
  (3600, 9876, '111222333444', 'G8', 2022, 'Leito'),
  (8106, 5432, '111333444555', 'G7', 2018, 'Cabine Cama'),
  (89068, 8765, '111333444555', 'G8', 2023, 'Cabine Cama'),
  (88089, 4321, '111333444555', 'G8', 2022, 'Semi-Leito'),
  (3515, 7890, '111222333444', 'G8', 2021, 'Leito'),
  (3420, 6543, '111222333444', 'G7', 2021, 'Leito'),
  (3220, 3456, '111222333444', 'G7', 2018, 'Leito'),
  (3640, 8901, '111222333444', 'G8', 2023, 'Leito');

Insert into viagem VALUES
  (1, 8106, '2023-11-01', '09:00', 113, 99, 50),
  (2, 3515, '2023-11-02', '10:30', 113, 324, 60),
  (3, 88089, '2023-11-03', '11:15', 113, 314, 70),
  (4, 3640, '2023-11-04', '14:00', 113, 575, 55),
  (5, 88009, '2023-11-05', '16:45', 1, 324, 65),
  (6, 86226, '2023-11-06', '18:30', 1, 323, 75),
  (7, 3420, '2023-11-07', '20:00', 15, 75, 70),
  (8, 3220, '2023-11-08', '22:15', 15, 1, 55),
  (9, 89068, '2023-11-09', '23:30', 3, 569, 10);

INSERT into motorista VALUES
  ('José', 'Silva', '118811', '12345678900', 1, 1),
  ('Maria', 'Santos', '212222', '98765432100', 2, 2),
  ('Pedro', 'Oliveira', '777333', '55555555500', 3, 3),
  ('Ana', 'Ferreira', '447444', '11111111100', 4, 4),
  ('Ricardo', 'Gomes', '553655', '77777777700', 5, 5),
  ('Camila', 'Rodrigues', '666666', '88888888800', 6, 6),
  ('Lucas', 'Fernandes', '775677', '99999999900', 7, 7),
  ('Isabela', 'Lima', '878888', '11122233300', 8, 8),
  ('Luis', 'Marcelo', '873786', '98765432101', 9, 9);


INSERT into bilhete VALUES
  (1, '111111', '2023-11-01', 1, 'func001'),
  (2, '999999', '2023-11-02', 2, 'func002'),
  (3, '777777', '2023-11-03', 3, 'func003'),
  (4, '212121', '2023-11-04', 4, 'func004'),
  (5, '171717', '2023-11-05', 5, 'func005'),
  (6, '191919', '2023-11-06', 6, 'func006'),
  (7, '333333', '2023-11-07', 7, 'func007'),
  (8, '999999', '2023-11-08', 8, 'func008'),
  (9, '131313', '2023-11-09', 1, 'func009'),
  (10, '222222', '2023-11-10', 2, 'func010'),
  (11, '212121', '2023-11-11', 9, 'func011')
  