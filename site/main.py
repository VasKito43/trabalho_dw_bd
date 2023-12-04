from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vascogabriel43:PmDw8gknVr3b@ep-dry-scene-49620356.us-east-2.aws.neon.tech/rodoviaria?sslmode=require'
db = SQLAlchemy(app)

class Cidade(db.Model):
    nome = db.Column(db.String(50),nullable=False)
    estado = db.Column(db.String(50),nullable=False)
    ccodigo = db.Column(db.Integer,primary_key=True, nullable=False)

class Empresa(db.Model):
    cnpj = db.Column(db.String(30),primary_key=True, nullable=False)
    nome = db.Column(db.String(50),nullable=False)
    cidade_codigo = db.Column(db.Integer, ForeignKey('cidade.ccodigo'), nullable=False)
    cidade = relationship("Cidade")

     #FOREIGN KEY (cidade) REFERENCES cidade(ccodigo)

class Onibus(db.Model):
    nonibus = db.Column(db.Integer,primary_key=True, nullable=False)
    placa = db.Column(db.Integer,nullable=False)
    empresa_cnpj = db.Column(db.String(30), ForeignKey('empresa.cnpj'), nullable=False)
    empresa = relationship("Empresa")
    modelo = db.Column(db.String(20), nullable=False)
    ano = db.Column(db.Integer,nullable=False)
    classe = db.Column(db.String(15), nullable=False)
    #FOREIGN KEY (empresa) REFERENCES empresa(cnpj)

class Cliente (db.Model):
    pnome = db.Column(db.String(50), nullable=False)
    unome = db.Column(db.String(50), nullable=False)
    rg = db.Column(db.String(20), nullable=False, primary_key=True)
    cpf = db.Column(db.String(20), nullable=False)
    datanasc = db.Column(db.DateTime)
    telefone = db.Column(db.String(20), nullable=False)

class Funcionario (db.Model):
    fcodigo = db.Column(db.String(10), nullable=False, primary_key=True)
    senha = db.Column(db.String(10), nullable=False)
    pnome = db.Column(db.String(50), nullable=False)
    unome = db.Column(db.String(50), nullable=False)
    rg = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(20), nullable=False)
    empresa_cnpj = db.Column(db.String(30), ForeignKey('empresa.cnpj'), nullable=False)
    empresa = relationship("Empresa")
    cidade_codigo = db.Column(db.Integer, ForeignKey('cidade.ccodigo'), nullable=False)
    cidade = relationship("Cidade")
    #   FOREIGN KEY (empresa) REFERENCES empresa(cnpj)
    #   FOREIGN KEY (cidade)  REFERENCES cidade(ccodigo)


    # usuario_id = Column(Integer, ForeignKey('usuario.id'))
    # usuario = relationship("Usuario", back_populates="contatos")

class Viagem (db.Model):
    cviagem = db.Column(db.Integer, nullable=False, primary_key=True)
    nonibus = db.Column(db.Integer, ForeignKey('onibus.nonibus'), nullable=False)
    onibus = relationship("Onibus")
    data = db.Column(db.DateTime,  nullable=False)
    horario = db.Column(db.String(5), nullable=False)
    origem = db.Column(db.Integer, ForeignKey('cidade.ccodigo'), nullable=False)
    destino = db.Column(db.Integer, ForeignKey('cidade.ccodigo'), nullable=False)
    cidade_origem = relationship("Cidade", foreign_keys=[origem])
    cidade_destino = relationship("Cidade", foreign_keys=[destino])
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
    cviagem = db.Column(db.Integer, ForeignKey('viagem.cviagem'), nullable=False)
    viagem = relationship("Viagem")
    #FOREIGN KEY (cviagem) REFERENCES viagem(cviagem)

class Bilhete (db.Model):
    nbbilhete = db.Column(db.Integer, nullable=False, primary_key=True)
    rgcliente = db.Column(db.String(20), ForeignKey('cliente.rg'), nullable=False)
    cliente = relationship("Cliente")
    datavenda = db.Column(db.DateTime, nullable=False)
    cviagem = db.Column(db.Integer, nullable=False)
    vendedor = db.Column(db.String(10), ForeignKey('funcionario.fcodigo'), nullable=False)
    funcionario = relationship("Funcionario")
# FOREIGN key (vendedor) REFERENCES funcionario(fcodigo)
# FOREIGN key (rg_cliente) REFERENCES cliente(rg)
# FOREIGN KEY (cviagem) REFERENCES viagem(cviagem)

@app.route('/')
def index():
    with app.app_context():
        todas_tabelas = Viagem.query.all()
        return render_template('pagina_principal.html', tabelas = todas_tabelas)
    
@app.route('/clientes_json', methods=['GET'])
def get_clientes():
    global lista_clientes
    with app.app_context():
        clientes = Cliente.query.all()
        clientes_list = [{"pnome": cliente.pnome, "unome": cliente.unome, "rg": cliente.rg, "cpf": cliente.cpf, "data_nasc": cliente.datanasc, "telefone": cliente.telefone} for cliente in clientes]
        return jsonify(clientes_list)
    
@app.route('/templates/menu/cadastro.html', methods=['GET'])
def carega_cadastro():    
    with app.app_context():
        return render_template('menu/cadastro.html')
    
@app.route('/templates/menu/funcionario.html', methods=['GET'])
def carrega_funcionario():
    with app.app_context():
        return render_template('menu/funcionario.html')
    
@app.route('/templates/menu/Funcionario/modifica-deleta_cadastro.html', methods=['GET'])
def carrega_mod_dlt_cad():
    with app.app_context():
        return render_template('menu/Funcionario/modifica-deleta_cadastro.html')
    
@app.route('/templates/menu/Funcionario/consultar.html', methods=['GET'])
def carrega_consultar():
    with app.app_context():
        return render_template('menu/Funcionario/consultar.html')
    

#consultas
    
# @app.route('/templates/menu/Funcionario/consultas/cidades_cadastradas.html', methods=['GET'])
# def carrega_consultar():
#     with app.app_context():
#         return render_template('menu/Funcionario/consultas/cidades_cadastradas.html')
    
# @app.route('/templates/menu/Funcionario/consultas/consulta_cadastro.html', methods=['GET'])
# def carrega_consultar():
#     with app.app_context():
#         return render_template('menu/Funcionario/consultas/consulta_cadastro.html')

# @app.route('/templates/menu/Funcionario/consultas/consultar_funcionario.html', methods=['GET'])
# def carrega_consultar():
#     with app.app_context():
#         return render_template('menu/Funcionario/consultas/consultar_funcionario.html')

# @app.route('/templates/menu/Funcionario/consultas/consultar_viagem.html', methods=['GET'])
# def carrega_consultar():
#     with app.app_context():
#         return render_template('menu/Funcionario/consultas/consultar_viagem.html')

# @app.route('/templates/menu/Funcionario/consultas/empresa_e_sede.html', methods=['GET'])
# def carrega_consultar():
#     with app.app_context():
#         return render_template('menu/Funcionario/consultas/empresa_e_sede.html')

# @app.route('/templates/menu/Funcionario/consultas/funcionario_e_sua_cidade.html', methods=['GET'])
# def carrega_consultar():
#     with app.app_context():
#         return render_template('menu/Funcionario/consultas/funcionario_e_sua_cidade.html')
    
# @app.route('/templates/menu/Funcionario/consultas/motorista_viagem_onibus.html', methods=['GET'])
# def carrega_consultar():
#     with app.app_context():
#         return render_template('menu/Funcionario/consultas/motorista_viagem_onibus.html')
    
# @app.route('/templates/menu/Funcionario/consultas/onibus_e_empresa.html', methods=['GET'])
# def carrega_consultar():
#     with app.app_context():
#         return render_template('menu/Funcionario/consultas/onibus_e_empresa.html')

# @app.route('/templates/menu/Funcionario/consultas/passageiros_da_viagem.html', methods=['GET'])
# def carrega_consultar():
#     with app.app_context():
#         return render_template('menu/Funcionario/consultas/passageiros_da_viagem.html')
    
# @app.route('/templates/menu/Funcionario/consultas/todos_os_bilhetes_do_cliente.html', methods=['GET'])
# def carrega_consultar():
#     with app.app_context():
#         return render_template('menu/Funcionario/consultas/todos_os_bilhetes_do_cliente.html')

# @app.route('/templates/menu/Funcionario/consultas/todos_os_bilhetes_do_funcionario.html', methods=['GET'])
# def carrega_consultar():
#     with app.app_context():
#         return render_template('menu/Funcionario/consultas/todos_os_bilhetes_do_funcionario.html')

# @app.route('/templates/menu/Funcionario/consultas/todos_os_clientes_por_ano.html', methods=['GET'])
# def carrega_consultar():
#     with app.app_context():
#         return render_template('menu/Funcionario/consultas/todos_os_clientes_por_ano.html')



@app.route('/cadastro', methods=['POST'])
def add_cliente():
    with app.app_context():
        if request.method == 'POST':
            nome = request.form['nome']
            sobrenome = request.form['sobrenome']
            cpf = request.form['documento_cpf']
            rg = request.form['documento_rg']
            datanasc = request.form['data_nasc']
            telefone = request.form['telefone']
            cliente = Cliente(pnome=nome, unome=sobrenome, cpf=cpf, rg=rg, datanasc=datanasc, telefone=telefone)
            db.session.add(cliente)
            db.session.commit()
            return render_template('menu/cadastro.html')
        

@app.route('/modifica-deleta_cadastro', methods=['POST', 'GET'])
def pesq_cliente():
    with app.app_context():

        clientes_pesquisa = None

        if request.method == 'POST':
            nome = request.form['nome']
            sobrenome = request.form['sobrenome']
            rg = request.form['rg']
            clientes_pesquisa = Cliente.query.filter_by(pnome=nome, unome=sobrenome, rg=rg).all()

        return render_template('menu/Funcionario/modifica-deleta_cadastro.html', clientes_pesquisa=clientes_pesquisa)
    
@app.route('/menu/Funcionario/edit_cliente/<string:rg>', methods=['GET', 'POST'])
def edit_cliente(rg):
    with app.app_context():
        cliente = Cliente.query.get(rg)
        if request.method == 'POST':
            cliente.pnome = request.form['nome']
            cliente.unome = request.form['sobrenome']
            cliente.cpf = request.form['documento_cpf']
            cliente.telefone = request.form['telefone']
            db.session.commit()
            return redirect('/')
        return render_template('menu/Funcionario/edit_cliente.html', cliente=cliente)



@app.route('/menu/Funcionario/delete_cliente/<string:rg>')
def delete_cliente(rg):
    with app.app_context():
        cliente = Cliente.query.get(rg)
        db.session.delete(cliente)
        db.session.commit()
        return redirect('/')







if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)