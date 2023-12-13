from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey, or_, and_
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


class Motorista(db.Model):
    pnome = db.Column(db.String(50), nullable=False)
    unome = db.Column(db.String(50),nullable=False)
    rg = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(20),primary_key=True, nullable=False)
    nmotorista = db.Column(db.Integer,nullable=False)
    cviagem = db.Column(db.Integer, ForeignKey('viagem.cviagem'), nullable=False)
    viagem = relationship("Viagem")

class Bilhete (db.Model):
    nbbilhete = db.Column(db.Integer, nullable=False, primary_key=True)
    rgcliente = db.Column(db.String(20), ForeignKey('cliente.rg'), nullable=False)
    cliente = relationship("Cliente")
    datavenda = db.Column(db.DateTime, nullable=False)
    cviagem = db.Column(db.Integer, nullable=False)
    vendedor = db.Column(db.String(10), ForeignKey('funcionario.fcodigo'), nullable=False)
    funcionario = relationship("Funcionario")





















@app.route('/')
def index():
    with app.app_context():
        todas_tabelas = Viagem.query.all()
        return render_template('pagina_principal.html', tabelas = todas_tabelas)
    
@app.route('/templates/menu/alunos.html', methods=['GET'])
def carega_alunos():    
    with app.app_context():
        return render_template('menu/alunos.html')    
    
@app.route('/templates/menu/conceitos.html', methods=['GET'])
def carega_conceitos():    
    with app.app_context():
        return render_template('/menu/conceitos.html')
    
@app.route('/templates/menu/banco_de_dados.html', methods=['GET'])
def carega_banco_de_dados():    
    with app.app_context():
        return render_template('/menu/banco_de_dados.html')

    
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
    
#cidade cadastradas
@app.route('/templates/menu/Funcionario/consultas/cidades_cadastradas.html', methods=['GET'])
def carrega_consulta_cidades_cadastradas():
    with app.app_context():
        return render_template('menu/Funcionario/consultas/cidades_cadastradas.html')
    
@app.route('/cidades_cadastradas', methods=['POST', 'GET'])
def consulta_cidades_cadastradas():
    with app.app_context():

        cidades_pesquisa = None

        if request.method == 'POST':
            nome = request.form['nome']
            ccodigo = request.form['ccodigo']
            if nome == '' and ccodigo == '':
                cidades_pesquisa = Cidade.query.all()
            else:
                if ccodigo != '':
                    cidades_pesquisa = Cidade.query.filter(and_(Cidade.nome.like(f'%{nome}%'),
                                                                Cidade.ccodigo == ccodigo)).all()
                else:
                    cidades_pesquisa = Cidade.query.filter(
                        Cidade.nome.like(f'%{nome}%')).all()


        return render_template('menu/Funcionario/consultas/cidades_cadastradas.html', cidades_pesquisa=cidades_pesquisa)
    



#consulta cadastro
@app.route('/templates/menu/Funcionario/consultas/consulta_cadastro.html', methods=['GET'])
def carrega_consulta_cadastro():
    with app.app_context():
        return render_template('menu/Funcionario/consultas/consulta_cadastro.html')
    
@app.route('/consulta_cadastro', methods=['POST', 'GET'])
def consulta_cadastro():
    with app.app_context():

        clientes_pesquisa = None

        if request.method == 'POST':
            nome = request.form['nome']
            sobrenome = request.form['sobrenome']
            rg = request.form['rg']
            cpf = request.form['cpf']
            if nome == '' and sobrenome == '' and rg == '' and cpf == '':
                clientes_pesquisa = Cliente.query.all()
            else:
                clientes_pesquisa = Cliente.query.filter(and_(Cliente.pnome.like(f'%{nome}%'), 
                                                              Cliente.unome.like(f'%{sobrenome}%'), 
                                                              Cliente.rg.like(f'%{rg}%'),
                                                              Cliente.cpf.like(f'%{cpf}%'))).all()
                          
        return render_template('menu/Funcionario/consultas/consulta_cadastro.html', clientes_pesquisa=clientes_pesquisa)
    
    
    
    
    
    

#consulta funcionario
@app.route('/templates/menu/Funcionario/consultas/consulta_funcionario.html', methods=['GET'])
def carrega_consulta_funcionario():
    with app.app_context():
        return render_template('menu/Funcionario/consultas/consulta_funcionario.html')
    
@app.route('/consulta_funcionario', methods=['POST', 'GET'])
def consulta_funcionario():
    with app.app_context():
        funcionario_pesquisa = None

        if request.method == 'POST':
            nome = request.form['nome']
            sobrenome = request.form['sobrenome']
            fcodigo = request.form['fcodigo']
            if nome == '' and sobrenome == '' and fcodigo == '':
                funcionario_pesquisa = Funcionario.query.all()
            else:
                funcionario_pesquisa = Funcionario.query.filter(and_(Funcionario.pnome.like(f'%{nome}%'), 
                                                              Funcionario.unome.like(f'%{sobrenome}%'), 
                                                              Funcionario.fcodigo.like(f'%{fcodigo}%'))).all()
        return render_template('menu/Funcionario/consultas/consulta_funcionario.html', funcionario_pesquisa=funcionario_pesquisa)

#consulta viagem
@app.route('/templates/menu/Funcionario/consultas/consulta_viagem.html', methods=['GET'])
def carrega_consultar_viagem():
    with app.app_context():
        return render_template('menu/Funcionario/consultas/consulta_viagem.html')
    
@app.route('/consulta_viagem', methods=['POST', 'GET'])
def consulta_viagem():
    with app.app_context():
        viagem_pesquisa = None

        if request.method == 'POST':
            origem = request.form['origem']
            destino = request.form['destino']
            cviagem = request.form['cviagem']
            if origem == '' and destino == '' and cviagem == '':
                viagem_pesquisa = Viagem.query.all()
            else:
                    cidade_origem = Cidade.query.filter(and_(Cidade.nome.like(f'%{origem}%')))
                    for i in cidade_origem:
                        nome_origem = i.nome
                        cidade_origem = i.ccodigo
                    cidade_destino = Cidade.query.filter(and_(Cidade.nome.like(f'%{destino}%')))
                    for i in cidade_destino:
                        nome_destino = i.nome
                        cidade_destino = i.ccodigo
                    viagem_pesquisa = Viagem.query.filter(and_(Viagem.origem == cidade_origem,
                                                               Viagem.destino == cidade_destino,
                                                               Viagem.cviagem == cviagem)).all()
        return render_template('menu/Funcionario/consultas/consulta_viagem.html', viagem_pesquisa=viagem_pesquisa, nome_destino=nome_destino, nome_origem=nome_origem)

#consulta empresa e sede

@app.route('/templates/menu/Funcionario/consultas/empresas_e_sede.html', methods=['GET'])
def carrega_consultar_empresa_e_sede():
    with app.app_context():
        return render_template('menu/Funcionario/consultas/empresas_e_sede.html')
    
@app.route('/consulta_empresa_e_sede', methods=['POST', 'GET'])
def consulta_empresa_e_sede():
    with app.app_context():
        if request.method == 'POST':
            cnpj = request.form['empresa']
            if cnpj != '':
                empresa = Empresa.query.filter(and_(Empresa.cnpj.like(f'{cnpj}'))).all()
                for i in empresa:
                    sede = i.cidade_codigo
                    nome_empresa = i.nome

                cidade = Cidade.query.filter(and_(Cidade.ccodigo == sede)).all()
                for i in cidade:
                    nome_cidade = i.nome

                return render_template('menu/Funcionario/consultas/empresas_e_sede.html', nome_empresa=nome_empresa, nome_cidade=nome_cidade)

        

#consulta funcionario e sua cidade

@app.route('/templates/menu/Funcionario/consultas/funcionario_e_sua_cidade.html', methods=['GET'])
def carrega_consultar_funcionario_e_sua_cidade():
    with app.app_context():
        return render_template('menu/Funcionario/consultas/funcionario_e_sua_cidade.html')
    
@app.route('/consulta_funcionario_e_sede', methods=['POST', 'GET'])
def consulta_funcionario_e_sede():
    with app.app_context():

        if request.method == 'POST':
            
            fcodigo = request.form['fcodigo']
            if fcodigo != '':
                funcionario = Funcionario.query.filter(and_(Funcionario.fcodigo.like(f'%{fcodigo}%')))
                for i in funcionario:
                    fcodigo = i.fcodigo
                    cidade_codigo = i.cidade_codigo
                
                cidade = Cidade.query.filter(and_(Cidade.ccodigo == cidade_codigo)).all()
        return render_template('menu/Funcionario/consultas/funcionario_e_sua_cidade.html', cidade=cidade, fcodigo=fcodigo)
    
#consulta motorista, onibus e viagem

@app.route('/templates/menu/Funcionario/consultas/motorista_viagem_onibus.html', methods=['GET'])
def carrega_consultar_motorista_viagem_onibus():
    with app.app_context():
        return render_template('menu/Funcionario/consultas/motorista_viagem_onibus.html')
    
@app.route('/consulta_motorista_onibus_viagem', methods=['POST', 'GET'])
def consulta_motorista_onibus_viagem():
    with app.app_context():

        if request.method == 'POST':
            
            nmotorista = request.form['nmotorista']
            if nmotorista != '':
                motorista = Motorista.query.filter(and_(Motorista.nmotorista == nmotorista))
                for i in motorista:
                    cviagem = i.cviagem
                    pnome = i.pnome
                    unome = i.unome
                viagem = Viagem.query.filter(and_(Viagem.cviagem == cviagem))
                for i in viagem:
                    nonibus = i.nonibus               
        return render_template('menu/Funcionario/consultas/motorista_viagem_onibus.html', pnome=pnome, unome=unome, nonibus=nonibus, cviagem=cviagem)

#consulta onibus e empresa 

@app.route('/templates/menu/Funcionario/consultas/onibus_e_empresa.html', methods=['GET'])
def carrega_consultar_onibus_e_empresa():
    with app.app_context():
        return render_template('menu/Funcionario/consultas/onibus_e_empresa.html')
    
@app.route('/consulta_empresa_onibus', methods=['POST', 'GET'])
def consulta_empresa_onibus():
     with app.app_context():
          if request.method == 'POST':
              nonibus = request.form['nonibus']
              if nonibus != '':
                onibus = Onibus.query.filter(and_(Onibus.nonibus == nonibus))
                for i in onibus:
                    nonibus = i.nonibus
                    placa = i.placa
                    empresa_cnpj = i.empresa_cnpj
                    classe = i.classe
                empresa = Empresa.query.filter(and_(Empresa.cnpj.like(f'%{empresa_cnpj}%')))
                for i in empresa:
                    nome = i.nome               
                return render_template('menu/Funcionario/consultas/onibus_e_empresa.html', nonibus=nonibus, placa=placa, classe=classe,  nome=nome)
               

         


#consulta passageiros da viagem

@app.route('/templates/menu/Funcionario/consultas/passageiros_da_viagem.html', methods=['GET'])
def carrega_consultar_passageiros_da_viagem():
    with app.app_context():
        return render_template('menu/Funcionario/consultas/passageiros_da_viagem.html')
    
    
@app.route('/consulta_passageiros_viagem', methods=['POST', 'GET'])
def passageiros_viagem():
     with app.app_context():
          cliente_list = []
          if request.method == 'POST':
              cviagem = request.form['cviagem']
              if cviagem != '':
                bilhete = Bilhete.query.filter(and_(Bilhete.cviagem == cviagem ))
                for i in bilhete:
                    rgcliente = i.rgcliente    
                    cliente = Cliente.query.filter(and_(Cliente.rg.like(f'{rgcliente}')))
                    cliente_list.append(cliente)
                return render_template('menu/Funcionario/consultas/passageiros_da_viagem.html', cliente_list=cliente_list )
    


# consulta todos os bilhetes de um funcionario

@app.route('/templates/menu/Funcionario/consultas/todos_os_bilhetes_do_cliente.html', methods=['GET'])
def carrega_bilhete_cliente():
    with app.app_context():
        return render_template('menu/Funcionario/consultas/todos_os_bilhetes_do_cliente.html')

@app.route('/todos_os_bilhetes_do_cliente', methods=['POST', 'GET'])
def pesq_bilhete_cliente():
    with app.app_context():
        if request.method == 'POST':
            rg = request.form['cliente']
            if rg == '':
                bilhete_pesquisa = ''
            else:
                bilhete_pesquisa = Bilhete.query.filter(and_(Bilhete.rgcliente.like(f'{rg}'))).all()
                return render_template('menu/Funcionario/consultas/todos_os_bilhetes_do_cliente.html', bilhete_pesquisa = bilhete_pesquisa)

#consulta todos os bilhetes de um funcionario

@app.route('/templates/menu/Funcionario/consultas/todos_os_bilhetes_do_funcionario.html', methods=['GET'])
def carrega_bilhete_funcionario():
    with app.app_context():
        return render_template('menu/Funcionario/consultas/todos_os_bilhetes_do_funcionario.html')

@app.route('/todos_os_bilhetes_do_funcionario', methods=['POST', 'GET'])
def pesq_bilhete():
    with app.app_context():
        if request.method == 'POST':
            id_funcionario = request.form['funcionario']
            if id_funcionario == '':
                bilhete_pesquisa = ''
            else:
                bilhete_pesquisa = Bilhete.query.filter(and_(Bilhete.vendedor.like(f'{id_funcionario}'))).all()
                return render_template('menu/Funcionario/consultas/todos_os_bilhetes_do_funcionario.html', bilhete_pesquisa = bilhete_pesquisa)

#consulta todos os clientes que viajaram por ano

@app.route('/templates/menu/Funcionario/consultas/todos_os_clientes_por_data.html', methods=['GET'])
def carrega_consultar_todos_os_clientes_por_data():
    with app.app_context():
        return render_template('menu/Funcionario/consultas/todos_os_clientes_por_data.html')
    
@app.route('/consulta_todos_os_clientes_por_data', methods=['POST', 'GET'])
def consulta_todos_os_clientes_por_data():
     with app.app_context():
          if request.method == 'POST':
              ano = request.form['ano']
              if ano != '':
                bilhete = Bilhete.query.filter(and_(Bilhete.datavenda == ano))
              
                return render_template('menu/Funcionario/consultas/todos_os_clientes_por_data.html', bilhete=bilhete)
    



#CRUD
@app.route('/cadastro', methods=['POST'])
def add_cliente():
    with app.app_context():
        if request.method == 'POST':
            nome = request.form['nome']
            sobrenome = request.form['sobrenome']
            rg = request.form['documento_rg']
            cpf = request.form['documento_cpf']
            datanasc = request.form['data_nasc']
            telefone = request.form['telefone']
            cliente = Cliente(pnome=nome, unome=sobrenome, rg=rg, datanasc=datanasc, telefone=telefone, cpf=cpf)
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