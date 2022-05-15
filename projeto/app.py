from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = "minha-chave"


# conexão com o banco de dados
app.config['MYSQL_Host'] = 'localhost'  # 127.0.0.1
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sua senha'  # muda aq pra sua senha
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
            flash("Dados Invalidos")
            return redirect('/login')
    else:
        return render_template('/login.html')

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastro(): ##################################################################### cadastro

    if request.method == 'POST':
        banco = request.form
        nome = banco['nome']
        email = banco['email']
        telefone = banco['telefone']
        senha = banco['senha']
        senha2 = banco['senha2'] 
        classe = 'Cliente'

        con = mysql.connection.cursor()
        if senha == senha2 :
            con.execute("INSERT INTO usuarios (nome, email, telefone, senha, classe ) VALUES (%s,%s,%s,%s,%s )",
                    (nome, email, telefone, senha, classe))
            mysql.connection.commit()
            con.close()

            flash("Cadastro Realizado!")
            return render_template("/cadastro.html")
        else:
            flash("Senhas não conferem! ")
            return render_template("/cadastro.html")

    else:
        return render_template("/cadastro.html")
        

##################################################### Executor  ##############################################


@app.route('/solicitacao_executor', methods=['GET', 'POST'])
def solicitacao_executor(): ######################################### Solicitação feita pelo executor 

    if request.method == 'POST':
    
        banco = request.form
        estado = 'Processando'
        resposta = 'Aguardando resposta'

        assunto = banco['assunto']
        descricao = banco['descricao']
        con = mysql.connection.cursor()
        con.execute(
            "INSERT INTO chamados (resposta_chamado, assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s, now(),%s,%s)", (resposta,assunto, descricao, id, estado,nome))
        mysql.connection.commit()
        con.close()
        flash("Solicitação enviada com sucesso!")
        return render_template("/solicitacao_executor.html")
    
    return render_template("/solicitacao_executor.html")


@app.route("/consulta_executor", methods=['GET'])
def consulta_executor(): ###################################lista com todas as solicitações feitas pelos usuarios
    
    cursor = mysql.connection.cursor()
    Values = cursor.execute("SELECT * FROM chamados where estado_chamado = 'Processando' and id_usuario !=%s order by data_de_inicio desc ",(id,) )
    
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
        estado = 'Finalizado'
        
        con = mysql.connection.cursor()
        
        con.execute(
            "UPDATE chamados SET data_de_termino =now(),nome_resposta =%s, id_usuario_resp =%s, resposta_chamado =%s, estado_chamado =%s where id_chamado =%s", (nome,id,diagnostico,estado,[ch]))
        mysql.connection.commit()
        con.close()
        return redirect('/consulta_executor')


@app.route('/reijeitar_solicitacao_exe/<ich>',methods=['POST'])
def bt_executor_reijeitar(ich): ################################# solicitação rejeitada pelo executor 

        banco = request.form
        diagnostico = banco['justifica']
        estado = 'Rejeitado'
        
        con = mysql.connection.cursor()
        
        con.execute(
            "UPDATE chamados SET data_de_termino =now(),nome_resposta =%s, id_usuario_resp =%s, estado_chamado =%s, resposta_chamado =%s where id_chamado =%s", (nome,id,estado,diagnostico,[ich]))
        mysql.connection.commit()
        con.close()
        return redirect('/consulta_executor')

################# ######################################### cliente #########################################

@app.route('/solicitacao_cliente', methods=['GET', 'POST'])
def solicitacao_cliente(): ######################################solicitação feita pelo cliente 
    
    if request.method == 'POST':

        banco = request.form
        estado = 'Processando'
        resposta = 'Aguardando resposta'
        

        assunto = banco['assunto']
        descricao = banco['descricao']
        con = mysql.connection.cursor()
        con.execute(
            "INSERT INTO chamados (resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s, now(),%s,%s)", (resposta,assunto, descricao, id, estado,nome))
        mysql.connection.commit()
        con.close()
        flash("Solicitação enviada com sucesso!")
        return render_template("/solicitacao_cliente.html")
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
    return render_template('solicitacao_cliente', Values=Values)


@app.route("/visualizar_solicitacao_cli/", methods=['GET','POST'])
def visualizar_cliente(): #tela de visualização de solicitação de cliente 
    return render_template('vsolicitacao_cliente')
    
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
    Values = cursor.execute("SELECT * FROM chamados Where id_usuario_resp = %s order by data_de_termino desc", (id,))
    
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

    if request.method == 'POST':
    
        banco = request.form
        estado = 'Processando'
        resposta = 'Aguardando resposta' 

        assunto = banco['assunto']
        descricao = banco['descricao']
        con = mysql.connection.cursor()
        con.execute(
            "INSERT INTO chamados (resposta_chamado,assunto, descricao, id_usuario, data_de_inicio, estado_chamado, nome_usuario ) VALUES (%s,%s,%s,%s, now(),%s,%s)", (resposta,assunto, descricao, id, estado,nome))
        mysql.connection.commit()
        con.close()
        flash("Solicitação enviada com sucesso!")
        return render_template("/solicitacao_administrador.html")
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
    tipo = con.fetchone()
    if tipo[0] == 'Técnico':
        con.execute(
            "UPDATE usuarios SET classe  = 'Cliente' WHERE id_usuario =%s ",(id,)) 
        mysql.connection.commit()
    else:
        con.execute(
            "UPDATE usuarios SET classe  = 'Técnico' WHERE id_usuario =%s ",(id,)) 
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
        estado = 'Finalizado'
        
        con = mysql.connection.cursor()
        
        con.execute(
            "UPDATE chamados SET data_de_termino =now(), id_usuario_resp =%s, nome_resposta =%s, resposta_chamado =%s, estado_chamado =%s where id_chamado =%s", (id,nome, diagnostico,estado,[ch]))
        mysql.connection.commit()
        con.close()
        return redirect('/admresponde')


@app.route('/reijeitar_resposta_adm/<ic>',methods=['POST'])
def bt_adm_reijeitar(ic): #######################################solicitação rejeitada pelo ADM 

        
        banco = request.form
        diagnostico = banco['justifica']
        estado = 'Rejeitado'
        
        con = mysql.connection.cursor()
        
        con.execute(
            "UPDATE chamados SET data_de_termino =now(),nome_resposta =%s, id_usuario_resp =%s, estado_chamado =%s, resposta_chamado =%s where id_chamado =%s", (nome,id,estado,diagnostico,[ic]))
        mysql.connection.commit()
        con.close()
        return redirect('/admresponde')



@app.route("/grafico") #rota do grafico
def grafico():
    global Finalizados
    global Recusados
    global Pendentes

    cursor = mysql.connection.cursor()
    Finalizados = cursor.execute("SELECT estado_chamado FROM chamados WHERE estado_chamado='Finalizado' ; ")
    Recusados = cursor.execute("SELECT estado_chamado FROM chamados WHERE estado_chamado='Rejeitado' ; ")
    Pendentes = cursor.execute("SELECT estado_chamado FROM chamados WHERE estado_chamado='Processando' ; ")

    data = [('Pendentes',Pendentes),('Finalizados', Finalizados), ('Recusados',Recusados)]
    if Finalizados == 0 and Recusados == 0 and Pendentes == 0:
      flash("Não há dados!")
      return render_template('graficos.html', data=data)

    return render_template('graficos.html',Finalizados=Finalizados,Recusados=Recusados,Pendentes=Pendentes,data=data)


    ################################################# Alteração de dados (cliente) #################################################

@app.route('/altera_cli', methods=['GET', 'POST'])
def altera_cli(): 

    if request.method == 'POST': 
        banco = request.form
        name = banco['nome']
        email = banco['email']
        telefone = banco['telefone']
        senha = banco['senha']
        senha2 = banco['senha2'] 
        

        con = mysql.connection.cursor()
        if senha == senha2 :
            con.execute( "UPDATE usuarios SET nome =%s, email =%s, telefone =%s, senha =%s where id_usuario =%s", (name,email,telefone,senha,id))

            mysql.connection.commit()
            con.close()

            flash("Cadastro Atualizado!")
            return render_template("/login.html")
        else:
            flash("Senhas não conferem! ")
            return render_template("/altera_cli.html")

    else:
        
        return render_template('/altera_cli.html')


    ################################################# Alteração de dados (executor) #################################################

@app.route('/altera_exe', methods=['GET', 'POST'])
def altera_exe(): 

    if request.method == 'POST': 
        banco = request.form
        name = banco['nome']
        email = banco['email']
        telefone = banco['telefone']
        senha = banco['senha']
        senha2 = banco['senha2'] 
        

        con = mysql.connection.cursor()
        if senha == senha2 :
            con.execute( "UPDATE usuarios SET nome =%s, email =%s, telefone =%s, senha =%s where id_usuario =%s", (name,email,telefone,senha,id))

            mysql.connection.commit()
            con.close()

            flash("Cadastro Atualizado!")
            return render_template("/login.html")
        else:
            flash("Senhas não conferem! ")
            return render_template("/altera_exe.html")

    else:
        
        return render_template('/altera_exe.html')
    

    
