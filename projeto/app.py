from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = "minha-chave"


# conexão com o banco de dados
app.config['MYSQL_Host'] = 'localhost'  # 127.0.0.1
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nai123'  # muda aq pra sua senha
app.config['MYSQL_DB'] = 'API'


mysql = MySQL(app)


@app.route("/")
@app.route('/login', methods=['GET', 'POST'])


def login(): ############################################################### Login

    global id 
    global nome
   
     
    if request.method == 'POST':
        banco = request.form
        email = banco['email']
        senha = banco['senha']

        con = mysql.connection.cursor()

        cliente = con.execute(
            "SELECT * FROM usuarios WHERE email = %s AND senha = %s AND classe='Cliente'", (email, senha,))
        executor = con.execute(
            "SELECT * FROM usuarios WHERE email = %s AND senha = %s AND classe='Técnico'", (email, senha,))
        adm = con.execute(
            "SELECT * FROM usuarios WHERE email = %s AND senha = %s AND classe='Administrador'", (email, senha,))
        con.close()

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s AND senha = %s ", (email, senha,))
        id = cursor.fetchall()

        cur = mysql.connection.cursor()
        cur.execute("SELECT nome FROM usuarios WHERE email = %s AND senha = %s", (email, senha,))
        nome = cur.fetchall()
        

        if cliente > 0:
            # return "cliente"
            return render_template('solicitacao_cliente.html')

        elif executor > 0:
            # return "executor"
                return redirect('consulta_executor')
        
        elif adm > 0:
                # return "executor"
            return render_template('solicitacao_administrador.html')


        else:
            flash("Dados Inválidos")
            return redirect('/login')
    else:
        return render_template('/login.html')

@app.route('/btcadastro', methods=['GET', 'POST'])
def bcadastro():
    return render_template('/cadastro.html')


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastro(): ##################################################################### cadastro

   
    if request.method == 'POST':
        banco = request.form
        nome = banco['nome']
        email = banco['email']
        senha = banco['senha']
        senha2 = banco['senha2'] 
        classe = 'Cliente'

        con = mysql.connection.cursor()
        emaildb = con.execute("SELECT email FROM usuarios WHERE email = %s", (email,))
        if emaildb:
            flash("Email já cadastrado! ")
            return render_template("/cadastro.html") 

        elif senha != senha2:
            flash("Senhas não conferem! ")
            return render_template("/cadastro.html")
        
        elif senha == senha2 :
            con.execute("INSERT INTO usuarios (nome, email, senha, classe ) VALUES (%s,%s,%s,%s )",
                    (nome, email, senha, classe))
            mysql.connection.commit()
            con.close()

            flash("Cadastro Realizado!")
            return render_template("/cadastro.html ")      
        
    else:
        return render_template("/cadastro.html")
        

##################################################### Executor  ##############################################


@app.route('/solicitacao_executor', methods=['GET', 'POST'])
def solicitacao_executor(): ######################################### Solicitação feita pelo executor 
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_chamado FROM chamados " )
    ids_cham = cursor.fetchall()
    cursor.execute("SELECT id_usuario FROM usuarios Where classe = 'Técnico' and id_usuario !=%s ",(id,)  )
    ids_exec = cursor.fetchall()
    cursor.execute("SELECT id_usuario FROM usuarios Where classe = 'Administrador'; ")
    adm = cursor.fetchone()

    if request.method == 'POST':
        banco = request.form
        estado = 'Processando'
        resposta = 'Aguardando resposta'
        assunto = banco['assunto']
        descricao = banco['descricao']


        if len(ids_exec) == 0:
                #comando para inserir no banco
            con = mysql.connection.cursor()
            con.execute(
                "INSERT INTO chamados (id_usuario_resp, assunto, descricao,resposta_chamado, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (adm,assunto, descricao, resposta, id, estado,nome))
            mysql.connection.commit()
            con.close()
            flash("Solicitação enviada com sucesso!")
            return redirect("/solicitacao_executor")
            


        elif len(ids_exec) == 1:
            execone = ids_exec[0]
            # commita no banco
            con = mysql.connection.cursor()
            con.execute(
                "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (execone,resposta,assunto, descricao, id, estado,nome))
            mysql.connection.commit()
            con.close()
            flash("Solicitação enviada com sucesso!")
            return redirect("/solicitacao_executor")

        else:
            if  len(ids_cham) >= 1:
                cursor.execute("SELECT id_usuario_resp FROM chamados ORDER BY id_chamado DESC LIMIT 2")
                ultimochamado = cursor.fetchall()
                print(ultimochamado)

                for i in range(len(ids_exec)):
                    if not ids_exec in ultimochamado:
                        if ids_exec[i] == ultimochamado[0]:
                            if ids_exec.index(ids_exec[i]) + 1 < len(ids_exec):
                                id_executor = ids_exec[i+1]
                                con = mysql.connection.cursor()
                                con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                mysql.connection.commit()
                                con.close()
                                flash("Solicitação enviada com sucesso!")
                                return redirect("/solicitacao_executor")

                            elif ids_exec.index(ids_exec[i]) + 2 > len(ids_exec):
                                id_executor = ids_exec[0]
                                con = mysql.connection.cursor()
                                con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                mysql.connection.commit()
                                con.close()
                                flash("Solicitação enviada com sucesso!")
                                return redirect("/solicitacao_executor")

                            elif  ids_exec.index(ids_exec[i]) + 1 == len(ids_exec):
                                    id_executor = ids_exec[-1]
                                    con = mysql.connection.cursor()
                                    con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                    mysql.connection.commit()
                                    con.close()
                                    flash("Solicitação enviada com sucesso!")
                                    return redirect("/solicitacao_executor")

                    else:
                        if ids_exec[i] == ultimochamado[1]:
                            if ids_exec.index(ids_exec[i]) + 1 < len(ids_exec):
                                id_executor = ids_exec[i+1]
                                con = mysql.connection.cursor()
                                con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                mysql.connection.commit()
                                con.close()
                                flash("Solicitação enviada com sucesso!")
                                return redirect("/solicitacao_executor")

                            elif ids_exec.index(ids_exec[i]) + 2 > len(ids_exec):
                                id_executor = ids_exec[0]
                                con = mysql.connection.cursor()
                                con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                mysql.connection.commit()
                                con.close()
                                flash("Solicitação enviada com sucesso!")
                                return redirect("/solicitacao_executor")

                            elif  ids_exec.index(ids_exec[i]) + 1 == len(ids_exec):
                                    id_executor = ids_exec[-1]
                                    con = mysql.connection.cursor()
                                    con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                    mysql.connection.commit()
                                    con.close()
                                    flash("Solicitação enviada com sucesso!")
                                    return redirect("/solicitacao_executor")

            else:
                for x in ids_exec:
                    id_executor = x
                    con = mysql.connection.cursor()
                    con.execute(
                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                    mysql.connection.commit()
                    con.close()
                    flash("Solicitação enviada com sucesso!")
                    return redirect("/solicitacao_executor")
    return render_template("/solicitacao_executor.html")


@app.route("/consulta_executor", methods=['GET'])
def consulta_executor(): ###################################lista com todas as solicitações feitas pelos usuarios
    
    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM chamados where estado_chamado = 'Processando' and id_usuario !=%s and id_usuario_resp =%s order by data_de_inicio desc ",(id,id,) )
    
    if Values > 0:
        Details = cursor.fetchall()
        return render_template('consulta_executor.html', Details=Details, Values=Values)
    flash("Não há dados!")
    return render_template('consulta_executor.html', Values=Values)



@app.route('/abrir_solicitacao_exe/<id>')
def bt_executor_visualizar(id): ########################################## visualizar  solicitação por completo 

    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM chamados WHERE id_chamado=%s",(id,))
    
    if Values > 0:
        Details = cursor.fetchall()
        return render_template('vsolicitacao_executor.html', Details=Details, Values=Values)
    return render_template('login.html', Values=Values)

        

@app.route("/visualizar_solicitacao_exe/<ch>", methods=['GET','POST'])
def visualizar_executor(ch): ################################################# resposta feita pelo executor
    
    

        banco = request.form
        diagnostico = banco['diagnostico']
 
        estado = banco ['bta'] 

        con = mysql.connection.cursor() 
            
        con.execute(
                "UPDATE chamados SET data_de_termino =now(), id_usuario_resp =%s, nome_resposta =%s, resposta_chamado =%s, estado_chamado =%s where id_chamado =%s", (id,nome, diagnostico,estado,[ch]))
        mysql.connection.commit()
        con.close()
        return redirect('/consulta_executor')

########################################################## cliente #########################################

####################### Funciona

@app.route('/solicitacao_cliente', methods=['GET', 'POST'])
def solicitacao_cliente(): ######################################solicitação feita pelo cliente 
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_chamado FROM chamados ")
    ids_cham = cursor.fetchall()
    cursor.execute("SELECT id_usuario FROM usuarios Where classe = 'Técnico'; ")
    ids_exec = cursor.fetchall()
    cursor.execute("SELECT id_usuario FROM usuarios Where classe = 'Administrador'; ")
    adm = cursor.fetchone()

    if request.method == 'POST':
        banco = request.form
        estado = 'Processando'
        resposta = 'Aguardando resposta'
        assunto = banco['assunto']
        descricao = banco['descricao']
        

        if len(ids_exec) == 0:
                #comando para inserir no banco
            con = mysql.connection.cursor()
            con.execute(
                "INSERT INTO chamados (id_usuario_resp, assunto, descricao,resposta_chamado, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (adm,assunto, descricao, resposta, id, estado,nome))
            mysql.connection.commit()
            con.close()
            flash("Solicitação enviada com sucesso!")
            return redirect("/solicitacao_cliente")
            


        elif len(ids_exec) == 1:
            execone = ids_exec[0]
            # commita no banco
            con = mysql.connection.cursor()
            con.execute(
                "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (execone,resposta,assunto, descricao, id, estado,nome))
            mysql.connection.commit()
            con.close()
            flash("Solicitação enviada com sucesso!")
            return redirect("/solicitacao_cliente")

        else:
            if  len(ids_cham) >= 1:
                cursor.execute("SELECT id_usuario_resp FROM chamados ORDER BY id_chamado DESC LIMIT 2")
                ultimochamado = cursor.fetchall()
                print(ultimochamado)

                for i in range(len(ids_exec)):
                    if not ids_exec in ultimochamado:
                        if ids_exec[i] == ultimochamado[0]:
                            if ids_exec.index(ids_exec[i]) + 1 < len(ids_exec):
                                id_executor = ids_exec[i+1]
                                con = mysql.connection.cursor()
                                con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                mysql.connection.commit()
                                con.close()
                                flash("Solicitação enviada com sucesso!")
                                return redirect("/solicitacao_cliente")

                            elif ids_exec.index(ids_exec[i]) + 2 > len(ids_exec):
                                id_executor = ids_exec[0]
                                con = mysql.connection.cursor()
                                con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                mysql.connection.commit()
                                con.close()
                                flash("Solicitação enviada com sucesso!")
                                return redirect("/solicitacao_cliente")

                            elif  ids_exec.index(ids_exec[i]) + 1 == len(ids_exec):
                                    id_executor = ids_exec[-1]
                                    con = mysql.connection.cursor()
                                    con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                    mysql.connection.commit()
                                    con.close()
                                    flash("Solicitação enviada com sucesso!")
                                    return redirect("/solicitacao_cliente")

                    else:
                        if ids_exec[i] == ultimochamado[1]:
                            if ids_exec.index(ids_exec[i]) + 1 < len(ids_exec):
                                id_executor = ids_exec[i+1]
                                con = mysql.connection.cursor()
                                con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                mysql.connection.commit()
                                con.close()
                                flash("Solicitação enviada com sucesso!")
                                return redirect("/solicitacao_cliente")

                            elif ids_exec.index(ids_exec[i]) + 2 > len(ids_exec):
                                id_executor = ids_exec[0]
                                con = mysql.connection.cursor()
                                con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                mysql.connection.commit()
                                con.close()
                                flash("Solicitação enviada com sucesso!")
                                return redirect("/solicitacao_cliente")

                            elif  ids_exec.index(ids_exec[i]) + 1 == len(ids_exec):
                                    id_executor = ids_exec[-1]
                                    con = mysql.connection.cursor()
                                    con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                    mysql.connection.commit()
                                    con.close()
                                    flash("Solicitação enviada com sucesso!")
                                    return redirect("/solicitacao_cliente")

            else:
                for x in ids_exec:
                    id_executor = x
                    con = mysql.connection.cursor()
                    con.execute(
                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                    mysql.connection.commit()
                    con.close()
                    flash("Solicitação enviada com sucesso!")
                    return redirect("/solicitacao_cliente")
    return render_template("/solicitacao_cliente.html")



@app.route("/consulta_cliente")
def consulta_cliente(): ######################################### lista com todas solicitações feitas pelo cliente 

    
    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM chamados Where id_usuario = %s order by data_de_inicio desc ", (id,))
    
    if Values > 0:
        cli = cursor.fetchall()
        return render_template('/consulta_cliente.html', cli=cli, Values=Values)
    flash("Não há dados!")
    return render_template('consulta_cliente.html', Values=Values)


    
@app.route('/abrir_solicitacao_cli/<id>')
def bt_cliente_visualizar(id): ############################### botão para cliente visualizar solicitação 

    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM chamados WHERE id_chamado=%s",(id,))
    
    if Values > 0:
        Details = cursor.fetchall()
        return render_template('vsolicitacao_cliente.html', Details=Details, Values=Values)
    return render_template('solicitacao_cliente.html', Values=Values)


@app.route("/visualizar_solicitacao_cli/", methods=['GET','POST'])
def visualizar_cliente(): #tela de visualização de solicitação de cliente 
    return redirect('vsolicitacao_cliente.html')
    
####################################################  executor (individual)  ############################################

@app.route("/consulta_executor1")
def consulta_executor1(): # lista com todas solicitações feitas pelo executor 

   
    
    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM chamados Where id_usuario = %s order by data_de_inicio desc ", (id,))
    
    if Values > 0:
        exe1 = cursor.fetchall()
        return render_template('/consulta_executor1.html', exe1 = exe1, Values=Values)
    flash("Não há dados!")
    return render_template('consulta_executor1.html', Values=Values)


    
@app.route('/abrir_solicitacao_exe1/<id>')
def bt_executor1_visualizar(id): #3################## botão para executor  visualizar suas solicitações  

    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM chamados WHERE id_chamado=%s",(id,))
    
    if Values > 0:
        Details = cursor.fetchall()
        return render_template('vsolicitacao_executor1.html', Details=Details, Values=Values)
    return render_template('solicitacao_executor', Values=Values)


@app.route("/visualizar_solicitacao_exe1/", methods=['GET','POST'])
def visualizar_executor1(): ############################### tela de visualização de solicitação do excutor  
    return render_template('vsolicitacao_executor1')



@app.route("/consulta_executor2")
def consulta_executor2(): ################################## lista solicitações respondidas pelo executor 

    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM chamados Where id_usuario_resp = %s and estado_chamado != 'Processando' order by data_de_termino desc", (id,))
    
    if Values > 0:
        exe1 = cursor.fetchall()
        return render_template('/consulta_executor2.html', exe1 = exe1, Values=Values)
    flash("Não há dados!")
    return render_template('consulta_executor2.html', Values=Values)


    
@app.route('/abrir_solicitacao_exe2/<id>')
def bt_executor2_visualizar(id): ###################################botão para abrir solicitação respondida pelo executor 

    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM chamados WHERE id_chamado=%s",(id,))
    
    if Values > 0:
        Details = cursor.fetchall()
        return render_template('vsolicitacao_executor2.html', Details=Details, Values=Values)
    return render_template('solicitacao_executor', Values=Values)


@app.route("/visualizar_solicitacao_exe2/", methods=['GET','POST'])
def visualizar_executor2(): #tela de visualização de solicitação de cliente 
    return render_template('vsolicitacao_executor2')





###################################################  Administrador ######################################################

@app.route('/solicitacao_administrador', methods=['GET', 'POST'])
def solicitacao_administrador(): #########################################  solicitação feita pelo ADM

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_chamado FROM chamados " )
    ids_cham = cursor.fetchall()
    cursor.execute("SELECT id_usuario FROM usuarios Where classe = 'Técnico' and id_usuario !=%s ",(id,)  )
    ids_exec = cursor.fetchall()

    if request.method == 'POST':
        banco = request.form
        estado = 'Processando'
        resposta = 'Aguardando resposta'
        assunto = banco['assunto']
        descricao = banco['descricao']



        if len(ids_exec) == 0:

            flash("Não há técnicos cadastrados!!")
            return redirect("/solicitacao_administrador")
            


        elif len(ids_exec) == 1:
            execone = ids_exec[0]
            # commita no banco
            con = mysql.connection.cursor()
            con.execute(
                "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (execone,resposta,assunto, descricao, id, estado,nome))
            mysql.connection.commit()
            con.close()
            flash("Solicitação enviada com sucesso!")
            return redirect("/solicitacao_administrador")

        else:
            if  len(ids_cham) >= 1:
                cursor.execute("SELECT id_usuario_resp FROM chamados ORDER BY id_chamado DESC LIMIT 2")
                ultimochamado = cursor.fetchall()
                print(ultimochamado)

                for i in range(len(ids_exec)):
                    if not ids_exec in ultimochamado:
                        if ids_exec[i] == ultimochamado[0]:
                            if ids_exec.index(ids_exec[i]) + 1 < len(ids_exec):
                                id_executor = ids_exec[i+1]
                                con = mysql.connection.cursor()
                                con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                mysql.connection.commit()
                                con.close()
                                flash("Solicitação enviada com sucesso!")
                                return redirect("/solicitacao_administrador")

                            elif ids_exec.index(ids_exec[i]) + 2 > len(ids_exec):
                                id_executor = ids_exec[0]
                                con = mysql.connection.cursor()
                                con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                mysql.connection.commit()
                                con.close()
                                flash("Solicitação enviada com sucesso!")
                                return redirect("/solicitacao_administrador")

                            elif  ids_exec.index(ids_exec[i]) + 1 == len(ids_exec):
                                    id_executor = ids_exec[-1]
                                    con = mysql.connection.cursor()
                                    con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                    mysql.connection.commit()
                                    con.close()
                                    flash("Solicitação enviada com sucesso!")
                                    return redirect("/solicitacao_administrador")

                    else:
                        if ids_exec[i] == ultimochamado[1]:
                            if ids_exec.index(ids_exec[i]) + 1 < len(ids_exec):
                                id_executor = ids_exec[i+1]
                                con = mysql.connection.cursor()
                                con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                mysql.connection.commit()
                                con.close()
                                flash("Solicitação enviada com sucesso!")
                                return redirect("/solicitacao_administrador")

                            elif ids_exec.index(ids_exec[i]) + 2 > len(ids_exec):
                                id_executor = ids_exec[0]
                                con = mysql.connection.cursor()
                                con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                mysql.connection.commit()
                                con.close()
                                flash("Solicitação enviada com sucesso!")
                                return redirect("/solicitacao_administrador")

                            elif  ids_exec.index(ids_exec[i]) + 1 == len(ids_exec):
                                    id_executor = ids_exec[-1]
                                    con = mysql.connection.cursor()
                                    con.execute(
                                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                                    mysql.connection.commit()
                                    con.close()
                                    flash("Solicitação enviada com sucesso!")
                                    return redirect("/solicitacao_administrador")

            else:
                for x in ids_exec:
                    id_executor = x
                    con = mysql.connection.cursor()
                    con.execute(
                        "INSERT INTO chamados (id_usuario_resp,resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s,%s, now(),%s,%s)", (id_executor,resposta,assunto, descricao, id, estado,nome))
                    mysql.connection.commit()
                    con.close()
                    flash("Solicitação enviada com sucesso!")
                    return redirect("/solicitacao_administrador")
    return render_template("/solicitacao_administrador.html")

@app.route("/consulta_administrador", methods=['GET'])
def consulta_administrador(): ################################# Mostra todas as solicitações que já foram finalizadas  

    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM chamados where estado_chamado = 'Finalizado' or  estado_chamado ='Rejeitado' order by data_de_termino desc")
    
    if Values > 0:
        Details = cursor.fetchall()
        return render_template('consulta_administrador.html', Details=Details, Values=Values)
    flash("Não há dados!")
    return render_template('consulta_administrador.html', Values=Values)


@app.route('/abrir_solicitacao_adm/<id>')
def bt_administrador_visualizar(id): ############################################abrir solicitação finalizada 

    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM chamados WHERE id_chamado=%s ",(id,))
    
    if Values > 0:
        Details = cursor.fetchall()
        return render_template('vsolicitacao_administrador.html', Details=Details, Values=Values)
    return render_template('login.html', Values=Values)


@app.route("/consulta_administrador1" )
def consulta_administrador1(): ################################### lista solicitações feitas pelo administrador 

    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM chamados Where id_usuario = %s order by data_de_inicio desc",  (id,))

    
    if Values > 0:
        exe1 = cursor.fetchall()
        return render_template('/consulta_administrador1.html', exe1 = exe1, Values=Values)
    flash("Não há dados!")
    return render_template('consulta_administrador1.html', Values=Values)


    
@app.route('/abrir_solicitacao_adm1/<id>')
def bt_administrador1_visualizar(id): ############################ botão para ADM visualizar solicitação 

    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM chamados WHERE id_chamado=%s",(id,))
    
    if Values > 0:
        Details = cursor.fetchall()
        return render_template('vsolicitacao_administrador1.html', Details=Details, Values=Values)
    return render_template('solicitacao_administrador', Values=Values)


@app.route("/visualizar_solicitacao_adm1/", methods=['GET','POST'])
def visualizar_administrador1(): #####################################tela de visualização de solicitação 
    return render_template('vsolicitacao_administrador1')


###################################################################################### - Altera cargo
@app.route("/config_adm/", methods=['GET','POST'])
def config_adm(): #mudar cliente para técnico

    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM usuarios where classe = 'Cliente' or  classe ='Técnico'")
    if Values > 0:
        usu = cursor.fetchall()
        return render_template('config_adm.html', usu=usu, Values=Values)

    flash("Não há dados!")
    return render_template('config_adm.html',Values=Values)


@app.route("/bt_mcargo/<id>", methods=['GET','POST']) ##############################botão mudar cargo
def mudar_cargo(id): 

    

    con = mysql.connection.cursor()
    con.execute("SELECT classe from usuarios where id_usuario =%s ",(id,))
    #adm = mysql.connection.cursor()

    tipo = con.fetchone()
    if tipo[0] == 'Técnico':
        con.execute(
            "UPDATE usuarios SET classe  = 'Cliente' WHERE id_usuario =%s ",(id,)) 
        mysql.connection.commit()
        con.close()
        con = mysql.connection.cursor()

        #pega os chamados
        cursorChamados = mysql.connection.cursor()
        chamados = []
        cursorChamados.execute("SELECT id_chamado FROM chamados WHERE id_usuario_resp = %s", (id,))
        for i in cursorChamados.fetchall():
            for chamado in i:
                chamados.append(chamado)
                print(f'chamado: {chamado}')
        
        cursorTecnicos = mysql.connection.cursor()
        tecnicos = []
        cursorTecnicos.execute("SELECT id_usuario FROM usuarios WHERE classe != 'Cliente' AND classe != 'Administrador' AND id_usuario != %s",(id,))
        for l in cursorTecnicos.fetchall():
            for tecnico in l:
                tecnicos.append(tecnico)
                print(f'tecnico: {tecnico}')
        
        cursorDistribuir = mysql.connection.cursor()
        if len(tecnicos) == 0:
            cursorAdmin = mysql.connection.cursor()
            cursorAdmin.execute("SELECT id_usuario FROM usuarios WHERE classe = 'Administrador'")
            admin = cursorAdmin.fetchone()
            print(admin)
            for chamado in chamados:
                print(chamado)  
                cursorDistribuir.execute("UPDATE chamados SET id_usuario_resp = %s WHERE id_chamado = %s", (admin,chamado,))
                mysql.connection.commit()
          
        if len(tecnicos) == 1:
            for chamado in chamados:
                cursorDistribuir.execute("UPDATE chamados SET id_usuario_resp = %s WHERE id_chamado = %s", (tecnicos[0],chamado))
                mysql.connection.commit()                  
        else:
            # listei todos chamados do ex tecnico
            for chamado in chamados:
                for tecnico in tecnicos:
                    cursorDistribuir.execute("UPDATE chamados SET id_usuario_resp = %s WHERE id_chamado = %s", (tecnico,chamados[0]))
                    #atribui um tecnico a um chamado
                    mysql.connection.commit()                  
                    del chamados[0]


         #Fazer update de  todos os id_usuario_resp desses chamados
    else:
        con.execute(
            "UPDATE usuarios SET classe  = 'Técnico' WHERE id_usuario =%s and classe != 'Administrador' ",(id,))  
        mysql.connection.commit()
    return redirect('/config_adm')



    ########################################################################## - adm responde solicitações


@app.route("/admresponde", methods=['GET'])
def consulta_administrador3(): #lista com todas as solicitações feitas pelos usuarios - executor e cliente
     
    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM chamados where estado_chamado = 'Processando' and id_usuario !=%s order by data_de_inicio desc ",(id,)  )
    
    if Values > 0:
        Details = cursor.fetchall()
        return render_template('consulta_administrador3.html', Details=Details, Values=Values)
    flash("Não há dados!")
    return render_template('consulta_administrador3.html', Values=Values)



@app.route('/abrir_adm_responde/<id>')
def bt_admresp_visualizar(id): ####################################rota para abrir solicitação por completo 

    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM chamados WHERE id_chamado=%s order by data_de_inicio desc",(id,))
    
    if Values > 0:
        Details = cursor.fetchall()
        return render_template('vsolicitacao_adm_responde.html', Details=Details, Values=Values)
    return render_template('login.html', Values=Values)

        

@app.route("/vrespostaadm/<ch>", methods=['GET','POST'])
def visualizar_administrador3(ch): ############################################resposta feita pelo ADM
    

        banco = request.form
        diagnostico = banco['diagnostico']
 
        estado = banco ['bta'] 

        con = mysql.connection.cursor() 
            
        con.execute(
                "UPDATE chamados SET data_de_termino =now(), id_usuario_resp =%s, nome_resposta =%s, resposta_chamado =%s, estado_chamado =%s where id_chamado =%s", (id,nome, diagnostico,estado,[ch]))
        mysql.connection.commit()
        con.close()
        return redirect('/admresponde')
   


    ################################################# Alteração de dados (cliente) #################################################

@app.route('/altera_cli', methods=['GET', 'POST'])
def altera_cli(): 

    if request.method == 'POST': 
        banco = request.form
        name = banco['nome']
        email = banco['email']
        senha = banco['senha']
        senha2 = banco['senha2'] 
        

        con = mysql.connection.cursor()
        emaildb = con.execute("SELECT email FROM usuarios WHERE email = %s", (email,))
        if emaildb:
            flash("Email já cadastrado! ")
            return render_template("/altera.cli.html") 

        elif senha != senha2:
            flash("Senhas não conferem! ")
            return render_template("/altera.cli.html")
        
        elif senha == senha2 :
            con.execute( "UPDATE usuarios SET nome =%s, email =%s, senha =%s where id_usuario =%s", (name,email,senha,id))

            mysql.connection.commit()
            con.close()
            
            flash("Cadastro Atualizado!")
            return render_template("/login.html")

    else:
        
        return render_template('/altera_cli.html')


    ################################################# Alteração de dados (executor) #################################################

@app.route('/altera_exe', methods=['GET', 'POST'])
def altera_exe(): 

    if request.method == 'POST': 
        banco = request.form
        name = banco['nome']
        email = banco['email']
        
        senha = banco['senha']
        senha2 = banco['senha2'] 
        

        con = mysql.connection.cursor()
        emaildb = con.execute("SELECT email FROM usuarios WHERE email = %s", (email,))
        if emaildb:
            flash("Email já cadastrado! ")
            return render_template("/altera.exe.html") 

        elif senha != senha2:
            flash("Senhas não conferem! ")
            return render_template("/altera.exe.html")
        
        elif senha == senha2 :
            con.execute( "UPDATE usuarios SET nome =%s, email =%s, senha =%s where id_usuario =%s", (name,email,senha,id))

            mysql.connection.commit()
            con.close()

            flash("Cadastro Atualizado!")
            return render_template("/login.html")


    else:
        
        return render_template('/altera_exe.html')

############################################################### Sistema de avaliação ##################################################################33


############################### Cliente
@app.route('/avaliar/<idsoli>')
def avaliar(idsoli): 
    return render_template("/starrating.html",idsoli=idsoli)

@app.route('/avaliando/<idsoli>', methods=['GET', 'POST'])
def avaliando(idsoli):
    coment_aval = request.form.get('comentario')
    estrela0=request.form.get('estrela0')
    estrela1=request.form.get('estrela1')
    estrela2=request.form.get('estrela2')
    estrela3=request.form.get('estrela3')
    estrela4=request.form.get('estrela4')
    estrela5=request.form.get('estrela5')
    x=[estrela0,estrela1,estrela2,estrela3,estrela4,estrela5]
    for i in x:
        if str(i) in "012345":
            con = mysql.connection.cursor()
            con.execute("UPDATE chamados SET avaliacao =%s, coment_aval=%s WHERE id_chamado = %s ",(i,coment_aval,idsoli,))
            mysql.connection.commit()
    return redirect("/consulta_cliente")


##################################### Adm

@app.route('/avaliaradm/<idsoli>')
def avaliaradm(idsoli): 
    return render_template("/starratingadm.html",idsoli=idsoli)

@app.route('/avaliandoadm/<idsoli>', methods=['GET', 'POST'])
def avaliandoadm(idsoli):
    coment_aval = request.form.get('comentario')
    estrela0=request.form.get('estrela0')
    estrela1=request.form.get('estrela1')
    estrela2=request.form.get('estrela2')
    estrela3=request.form.get('estrela3')
    estrela4=request.form.get('estrela4')
    estrela5=request.form.get('estrela5')
    x=[estrela0,estrela1,estrela2,estrela3,estrela4,estrela5]
    for i in x:
        if str(i) in "012345":
            con = mysql.connection.cursor()
            con.execute("UPDATE chamados SET avaliacao =%s, coment_aval=%s WHERE id_chamado = %s ",(i,coment_aval,idsoli,))
            mysql.connection.commit()
    return redirect("/consulta_administrador1")


########################################## Exe

@app.route('/avaliarexe/<idsoli>')
def avaliarexe(idsoli): 
    return render_template("/starratingexe.html",idsoli=idsoli)

@app.route('/avaliandoexe/<idsoli>', methods=['GET', 'POST'])
def avaliandoexe(idsoli):
    coment_aval = request.form.get('comentario')
    estrela0=request.form.get('estrela0')
    estrela1=request.form.get('estrela1')
    estrela2=request.form.get('estrela2')
    estrela3=request.form.get('estrela3')
    estrela4=request.form.get('estrela4')
    estrela5=request.form.get('estrela5')
    x=[estrela0,estrela1,estrela2,estrela3,estrela4,estrela5]
    for i in x:
        if str(i) in "012345":
            con = mysql.connection.cursor()
            con.execute("UPDATE chamados SET avaliacao =%s, coment_aval=%s WHERE id_chamado = %s ",(i,coment_aval,idsoli,))
            mysql.connection.commit()
    return redirect("/consulta_executor1")








############################################################################# Grafico ######################################################################333
from datetime import date, time, datetime, timedelta
import datetime

data_atual=datetime.date.today()  #pega a data atual
filtro = 'tudo'          #ele deve ser modificado de acordo como o menu lateral

@app.route("/grafico") #rota do grafico
def grafico():
    global Finalizados
    global Recusados
    global Pendentes

    cursor = mysql.connection.cursor()
    Finalizados = cursor.execute("SELECT estado_chamado FROM chamados WHERE estado_chamado='Finalizado' ; ")
    Recusados = cursor.execute("SELECT estado_chamado FROM chamados WHERE estado_chamado='Rejeitado' ; ")
    Pendentes = cursor.execute("SELECT estado_chamado FROM chamados WHERE estado_chamado='Processando' ; ")



    


    nestrela0 = cursor.execute("SELECT avaliacao FROM chamados WHERE avaliacao='0' ; ")
    nestrela1 = cursor.execute("SELECT avaliacao FROM chamados WHERE avaliacao='1' ; ") #pega a quantidade de estrelas e salva em varias variasveis
    nestrela2 = cursor.execute("SELECT avaliacao FROM chamados WHERE avaliacao='2' ; ")
    nestrela3 = cursor.execute("SELECT avaliacao FROM chamados WHERE avaliacao='3' ; ")
    nestrela4 = cursor.execute("SELECT avaliacao FROM chamados WHERE avaliacao='4' ; ")
    nestrela5 = cursor.execute("SELECT avaliacao FROM chamados WHERE avaliacao='5' ; ")
    nestrela6 = cursor.execute("SELECT avaliacao FROM chamados WHERE avaliacao='6' ; ") #pega a quantidade de estrelas e salva em varias variasveis
    nestrela7 = cursor.execute("SELECT avaliacao FROM chamados WHERE avaliacao='7' ; ")
    nestrela8 = cursor.execute("SELECT avaliacao FROM chamados WHERE avaliacao='8' ; ")
    nestrela9 = cursor.execute("SELECT avaliacao FROM chamados WHERE avaliacao='9' ; ")
    nestrela10 = cursor.execute("SELECT avaliacao FROM chamados WHERE avaliacao='10' ; ")

    #     #Aplicação do filtro:
    
    if filtro == 'dia':
        numerodedias= 0

    elif filtro == 'semana':
        numerodedias= 7

    elif filtro == '15d':
        numerodedias= 15

    elif filtro == 'mes':
        numerodedias= 30

    elif filtro == 'tudo':
        numerodedias= 99999
    else:
        numerodedias = 0       
    diferenca = timedelta(days=numerodedias)   
    testando=data_atual - diferenca   
    dia_desejado = testando

    FinalizadosF = cursor.execute("SELECT estado_chamado FROM chamados WHERE estado_chamado='Finalizado' and data_de_inicio >= %s; ",(dia_desejado,))
    RecusadosF = cursor.execute("SELECT estado_chamado FROM chamados WHERE estado_chamado='Rejeitado' and data_de_inicio >= %s; ",(dia_desejado,))
    PendentesF = cursor.execute("SELECT estado_chamado FROM chamados WHERE estado_chamado='Processando' and data_de_inicio >= %s; ",(dia_desejado,))

    Fechados = cursor.execute("SELECT estado_chamado FROM chamados WHERE estado_chamado!='Processando'and data_de_inicio >= %s; ",(dia_desejado,))
    Abertos = cursor.execute("SELECT estado_chamado FROM chamados WHERE estado_chamado='Processando'and data_de_inicio >= %s; ",(dia_desejado,))
   

    data = [('Abertos',Abertos),('Fechados',Fechados)] #salva os dados em uma array para serem usados no grafico
    data2 = [('0 Estrela',nestrela0),('1 Estrela',nestrela1),('2 Estrelas', nestrela2), ('3 Estrelas',nestrela3), ('4 Estrelas', nestrela4), ('5 Estrelas', nestrela5), ('6 Estrelas',nestrela6),('7 Estrelas', nestrela7), ('8 Estrelas',nestrela8), ('9 Estrelas', nestrela9), ('10 Estrelas', nestrela10)]

    if Finalizados == 0 and Recusados == 0 and Pendentes == 0:
      flash("Não há dados!")
      return render_template('graficos.html', data=data,data2=data2)

    return render_template('graficos.html',Finalizados=Finalizados,Recusados=Recusados,Pendentes=Pendentes,nestrela0=nestrela0,nestrela1=nestrela1,nestrela2=nestrela2,nestrela3=nestrela3,nestrela4=nestrela4,nestrela5=nestrela5,nestrela6=nestrela6,nestrela7=nestrela7,nestrela8=nestrela8,nestrela9=nestrela9,nestrela10=nestrela10,data=data,data2=data2,filtro=filtro)

# Antes ou depois de mudar um Técnico para cliente, pegar todos os chamados que ele tem e  por numa variavel
# Depois fazer um "for" e redistribuir pros usuarios que ainda são tecnicos



@app.route("/FiltroPizzaD", methods=["GET","POST"]) 
def graficoDia(): 
    global filtro
    filtrar = request.form
    filtro = filtrar['dia']

    return redirect ('/grafico')

@app.route("/FiltroPizzaS", methods=["GET","POST"]) 
def graficaSemana(): 
    global filtro
    filtrar = request.form
    filtro = filtrar['semana']

    return redirect ('/grafico')

@app.route("/FiltroPizza15", methods=["GET","POST"]) 
def grafica15d(): 
    global filtro
    filtrar = request.form
    filtro = filtrar['15d']

    return redirect ('/grafico')


@app.route("/FiltroPizzaM", methods=["GET","POST"]) 
def graficaMes(): 
    global filtro
    filtrar = request.form
    filtro = filtrar['mes']

    return redirect ('/grafico')

@app.route("/FiltroPizzaT", methods=["GET","POST"]) 
def graficaTudo(): 
    global filtro
    filtrar = request.form
    filtro = filtrar['tudo']

    return redirect ('/grafico')