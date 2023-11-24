from flask import Flask, render_template, redirect, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'com apenas um click'


@app.route('/')
def home():
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():

    nome = request.form.get('nome')
    sobrenome = request.form.get('sobrenome')
    doc_rg = request.form.get('documento_cpf')
    doc_rg = request.form.get('documento_rg')
    data_nasc = request.form.get('data_nasc')
    telefone = request.form.get('telefone')

    return render_template('cadastro.html', nome = nome, sobrenome = sobrenome, doc_rg = doc_rg, data_nasc = data_nasc, telefone = telefone)


if __name__ in "__main__":
    app.run(debug=True) 