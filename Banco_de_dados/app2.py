from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/rodoviaria'
db = SQLAlchemy(app)

class Cidade(db.Model):
    nome = db.Column(db.String(50),nullable=False)
    estado = db.Column(db.String(50),nullable=False)
    C_codigo = db.Column(db.Integer,primary_key=True, nullable=False)

class Empresa(db.Model):
    cnpj = db.Column(db.String(30),primary_key=True, nullable=False)
    nome = db.Column(db.String(50),nullable=False)
    cidade_codigo = db.Column(db.Integer, ForeignKey('cidade.C_codigo'), nullable=False)
    cidade = relationship("Cidade")

     #FOREIGN KEY (cidade) REFERENCES cidade(ccodigo)

class Onibus(db.Model):
    N_onibus = db.Column(db.Integer,primary_key=True, nullable=False)
    placa = db.Column(db.Integer,nullable=False)
    empresa_cnpj = db.Column(db.String(30), ForeignKey('empresa.cnpj'), nullable=False)
    empresa = relationship("Empresa")
    modelo = db.Column(db.String(20), nullable=False)
    ano = db.Column(db.Integer,nullable=False)
    classe = db.Column(db.String(15), nullable=False)
    #FOREIGN KEY (empresa) REFERENCES empresa(cnpj)

class Cliente (db.Model):
    p_nome = db.Column(db.String(50), nullable=False)
    U_nome = db.Column(db.String(50), nullable=False)
    rg = db.Column(db.String(20), nullable=False, primary_key=True)
    cpf = db.Column(db.String(20), nullable=False)
    data_nasc = db.Column(db.DateTime)
    telefone = db.Column(db.String(20), nullable=False)

class Funcionario (db.Model):
    F_codigo = db.Column(db.String(10), nullable=False, primary_key=True)
    senha = db.Column(db.String(10), nullable=False)
    P_nome = db.Column(db.String(50), nullable=False)
    U_nome = db.Column(db.String(50), nullable=False)
    rg = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(20), nullable=False)
    empresa_cnpj = db.Column(db.String(30), ForeignKey('empresa.cnpj'), nullable=False)
    empresa = relationship("Empresa")
    cidade_codigo = db.Column(db.Integer, ForeignKey('cidade.C_codigo'), nullable=False)
    cidade = relationship("Cidade")
    #   FOREIGN KEY (empresa) REFERENCES empresa(cnpj)
    #   FOREIGN KEY (cidade)  REFERENCES cidade(ccodigo)


    # usuario_id = Column(Integer, ForeignKey('usuario.id'))
    # usuario = relationship("Usuario", back_populates="contatos")

class Viagem (db.Model):
    C_viagem = db.Column(db.Integer, nullable=False, primary_key=True)
    N_onibus = db.Column(db.Integer, ForeignKey('onibus.N_onibus'), nullable=False)
    onibus = relationship("Onibus")
    data = db.Column(db.DateTime,  nullable=False)
    horario = db.Column(db.String(5), nullable=False)
    origem_codigo = db.Column(db.Integer, ForeignKey('cidade.C_codigo'), nullable=False)
    destino = db.Column(db.Integer, ForeignKey('cidade.C_codigo'), nullable=False)
    cidade = relationship("Cidade")
    preco = db.Column(db.Integer, nullable=False)
#    FOREIGN KEY (origem) REFERENCES cidade(ccodigo)
#    FOREIGN KEY (destino) REFERENCES cidade(ccodigo)
#    FOREIGN key (nonibus) REFERENCES onibus(nonibus)

class Motorista(db.Model):
    P_nome = db.Column(db.String(50), nullable=False)
    U_nome = db.Column(db.String(50),nullable=False)
    rg = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(20),primary_key=True, nullable=False)
    N_motorista = db.Column(db.Integer,nullable=False)
    C_viagem = db.Column(db.Integer, ForeignKey('viagem.C_viagem'), nullable=False)
    viagem = relationship("Viagem")
    #FOREIGN KEY (cviagem) REFERENCES viagem(cviagem)

class Bilhete (db.Model):
    N_bilhete = db.Column(db.Integer, nullable=False, primary_key=True)
    RG_cliente = db.Column(db.String(20), ForeignKey('cliente.rg'), nullable=False)
    cliente = relationship("Cliente")
    data_venda = db.Column(db.DateTime, nullable=False)
    C_viagem = db.Column(db.Integer, nullable=False)
    vendedor = db.Column(db.String(10), ForeignKey('funcionario.F_codigo'), nullable=False)
    funcionario = relationship("Funcionario")
# FOREIGN key (vendedor) REFERENCES funcionario(fcodigo)
# FOREIGN key (rg_cliente) REFERENCES cliente(rg)
# FOREIGN KEY (cviagem) REFERENCES viagem(cviagem)

with app.app_context():
    db.create_all()