from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)


# conexão com o banco de dados
app.config['MYSQL_Host'] = 'localhost' # 127.0.0.1
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'fatec'
app.config['MYSQL_DB'] = 'API'


mysql = MySQL(app)

@app.route("/")
@app.route("/Solicitacao")


@app.route("/index")
def lg_executor():
    return render_template("/index.html")

@app.route("/indeCliente")
def lg_cliente():
    return render_template("/index.html")


@app.route("/executor_solicitacao_recebida")
def soli_recebida(): 
    return render_template("/executor_solicitação_recebidas.html")   


@app.route("/Cliente_consulta")
def cliente_soli_recebida():
    return render_template("/consulta_cli.html") 


@app.route("/solicitacao_cliente")
def cliente_so():
    return render_template("solicitação_cli.html")

@app.route("/solicitação_exec")
def executor_so():
    return render_template("solicitação_exec.html")


''''@app.route('/criar', methods=['GET', 'POST'])
def cliente_sol():
    if request.method == 'POST':
        nome = request.form ['username']
        email = request.form ['email']
        assunto = request.form ['assunto']
        descricao = request.form ['descricao']
        con = mysql.connection.cursor()
        con.execute ("INSERT INTO chamados (nome_usuario, email_usuario, assunto, descricao) VALUES (%s,%s,%s,%s)",(nome, email, assunto, descricao))
        con.commit()

    return redirect("/solicitação_cliente")
    '''
@app.route('/teste1', methods=['GET', 'POST'])
def teste1():
    if request.method == 'POST':
        nome = request.form ['nome']
        email = request.form ['email']
        cur = mysql.connection.cursor()
        cur.execute ("INSERT INTO teste1 (nome, email) VALUES (%s,%s)",(nome, email))
        mysql.connection.commit()
        cur.close()
    return render_template("teste1.html")

      #if  request.method == 'POST':
