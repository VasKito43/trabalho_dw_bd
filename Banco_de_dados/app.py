from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/sql_python'
db = SQLAlchemy(app)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
# CREATE TABLE bilhete(
#           nbilhete int NOT NULL PRIMARY KEY,
#           rg_cliente varchar(20) NOT NULL,
#           data_venda date,
#           cviagem int NOT NULL,
#           vendedor varchar(10) NOT NULL,
#           FOREIGN key (vendedor) REFERENCES funcionario(fcodigo),
#           FOREIGN key (rg_cliente) REFERENCES cliente(rg),
#           FOREIGN KEY (cviagem) REFERENCES viagem(cviagem)
#         );
@app.route('/')
def index():
    with app.app_context():
        produtos = Produto.query.all()
        return render_template('index.html', produtos=produtos)

@app.route('/produtos_json', methods=['GET'])
def get_produtos():
    with app.app_context():
        produtos = Produto.query.all()
        produtos_list = [{"id": produto.id, "nome": produto.nome, "descricao": produto.descricao} for produto in produtos]
        return jsonify(produtos_list)

@app.route('/add_produto', methods=['POST'])
def add_produto():
    with app.app_context():
        if request.method == 'POST':
            nome = request.form['nome']
            descricao = request.form['descricao']
            produto = Produto(nome=nome, descricao=descricao)
            db.session.add(produto)
            db.session.commit()
            return redirect('/')

@app.route('/edit_produto/<int:id>', methods=['GET', 'POST'])
def edit_produto(id):
    with app.app_context():
        produto = Produto.query.get(id)
        if request.method == 'POST':
            produto.nome = request.form['nome']
            produto.descricao = request.form['descricao']
            db.session.commit()
            return redirect('/')
        return render_template('edit_produto.html', produto=produto)

@app.route('/delete_produto/<int:id>')
def delete_produto(id):
    with app.app_context():
        produto = Produto.query.get(id)
        db.session.delete(produto)
        db.session.commit()
        return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
