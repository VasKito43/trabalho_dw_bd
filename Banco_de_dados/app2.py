from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/rodoviaria'
db = SQLAlchemy(app)

class Cidade(db.Model):
    nome = db.Column(db.String(50),nullable=False)
    estado = db.Column(db.String(50),nullable=False)
    ccodigo = db.Column(db.Integer,primary_key=True, nullable=False)

class Empresa(db.Model):
    cnpj = db.Column(db.String(30),primary_key=True, nullable=False)
    nome = db.Column(db.String(50),nullable=False)
    cidade = db.Column(db.Integer, nullable=False)
     #FOREIGN KEY (cidade) REFERENCES cidade(ccodigo)

class Onibus(db.Model):
    nonibus = db.Column(db.Integer,primary_key=True, nullable=False)
    placa = db.Column(db.Integer,nullable=False)
    empresa = db.Column(db.String(30), nullable=False)
    modelo = db.Column(db.String(20), nullable=False)
    ano = db.Column(db.Integer,nullable=False)
    classe = db.Column(db.String(15), nullable=False)
    #FOREIGN KEY (empresa) REFERENCES empresa(cnpj)

class cliente (db.Model):
    p_nome = db.Column(db.String(50), nullable=False)
    U_nome = db.Column(db.String(50), nullable=False)
    rg = db.Column(db.String(20), nullable=False, primary_key=True)
    cpf = db.Column(db.String(20), nullable=False)
    data_nasc = db.Column(db.DateTime, default=datetime.utcnow)
    telefone = db.Column(db.String(20), nullable=False)

class funcionario (db.Model):
    F_codigo = db.Column(db.String(10), nullable=False, primary_key=True)
    senha = db.Column(db.String(10), nullable=False)
    P_nome = db.Column(db.String(50), nullable=False)
    U_nome = db.Column(db.String(50), nullable=False)
    rg = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(20), nullable=False)
    empresa_cnpj = db.Column(db.String(30), ForeignKey('empresa.cnpj'), nullable=False)
    empresa = relationship("empresa")
    cidade = db.Column(db.Integer, nullable=False)
    #   FOREIGN KEY (empresa) REFERENCES empresa(cnpj)
    #   FOREIGN KEY (cidade)  REFERENCES cidade(ccodigo)


    # usuario_id = Column(Integer, ForeignKey('usuario.id'))
    # usuario = relationship("Usuario", back_populates="contatos")

class viagem (db.Model):
    C_codigo = db.Column(db.Integer, nullable=False, primary_key=True)
    N_onibus = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    horario = db.Column(db.String(5), nullable=False)
    origem = db.Column(db.Integer, nullable=False)
    destino = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Integer, nullable=False)
#    FOREIGN KEY (origem) REFERENCES cidade(ccodigo)
#    FOREIGN KEY (destino) REFERENCES cidade(ccodigo)
#    FOREIGN key (nonibus) REFERENCES onibus(nonibus)

class Motorista(db.Model):
    pnome = db.Column(db.String(50), nullable=False)
    unome = db.Column(db.String(50),nullable=False)
    rg = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(20),primary_key=True, nullable=False)
    nmotorista = db.Column(db.Integer,nullable=False)
    cviagem = db.Column(db.Integer, nullable=False)
    #FOREIGN KEY (cviagem) REFERENCES viagem(cviagem)

class bilhete (db.Model):
    N_bilhete = db.Column(db.Integer, nullable=False, primary_key=True)
    RG_cliente = db.Column(db.Integer, nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    C_viagem = db.Column(db.Integer, nullable=False)
    vendedor = db.Column(db.String(10), nullable=False)
# FOREIGN key (vendedor) REFERENCES funcionario(fcodigo)
# FOREIGN key (rg_cliente) REFERENCES cliente(rg)
# FOREIGN KEY (cviagem) REFERENCES viagem(cviagem)


