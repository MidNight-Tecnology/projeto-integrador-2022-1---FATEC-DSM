<br id="topo">

![Logo da equipe Impulse Team](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/imagens%20read.me/Impulse%20Team%20logo.png)

<h1 align="center"> Sprint 2: 25/04/2022 a 15/05/2022 </h1>

<p align="center"> 
  <a href="#entrega"> Entregas de valor </a>             |                
  <a href="#planejamento"> Planejamento da Sprint </a>   |
  <a href="#execproje">Executando o Projeto</a>          |  
  <a href="#modbanco"> Modelagem de Banco de dados </a>  |
  <a href="#rotasfront"> Rotas de Python e Frontend </a> |
  <a href="#metequipe"> Métricas da Equipe </a>          |
  <a href="#apfinal"> Apresentação Final </a> </p>             

<br>

</br>
  
<span id="entrega">
🎯 <b>Entregas de valor</b>
<p></p>
<p> ✔️ Tela de login. </p> 	
<p> ✔️ Chamados enviados e respondidos, vinculados ao criador, ao técnico e com acesso total por parte do administrador do sistema. </p> 
<p> ✔️ Geração de relatório sobre os chamados. </p> 

→ [Voltar ao topo](#topo)
  
<br>
</br>
  
<span id="planejamento">
📑 <b>Planejamento da Sprint</b>
<p></p> 
  
![imagem backlog Sprint 2](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/Backlog%20Sprint%202%20-%20Impulse%20Team%20-%202022-1.png)  
  
  
→ [Voltar ao topo](#topo)

<br>
</br>

<span id="execproje">
📝 <b>Executando o Projeto</b>
<p></p>

Clone o repositório:
```bash
git clone https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM.git
```

Crie um ambiente virtual dentro da pasta projeto:
```bash
python -m venv env
```
Ative este ambiente virtual:
```bash
.\env\Scripts\activate
```
Instale as dependências do arquivo requirements.txt:
```bash
 pip install -r requirements.txt
```
Execute o sequintes comandos para iniciar:

```bash
 set FLASK_ENV=development
```

```bash
 flask run
```
Copie e cole o link na barra de endereço do seu navegador para visualizar o projeto:

```bash
 http://127.0.0.1:5000/
```

Execução do Banco de dados (MySQL):

```bash
 Inicie o arquivo app.py e coloque sua senha do MySQL no lugar marcado. 
```

```bash
 Inicie o MySQL, abra e execute o arquivo API.sql e crie o banco de dados.  
```
Depois da realização desses passos o sistema já está pronto para ser utilizado.

Login Administrador:
Alteração dos dados de acesso do administrador devem ser feitas diretamente no banco de dados.
	
```bash
Login padrão:	
	Login: adm@gmail.com
	Senha: adm
```
  
→ [Voltar ao topo](#topo)
  
<br>
</br>  
  
<span id="modbanco">
<b> Modelagem de Banco de dados </b>
<p></p> 
  
![Modelo Conceitual](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/Modelo%20Conceitual%20-%20%5BSP-02%5D.png)  
![Modelo Lógico](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/Modelo%20L%C3%B3gico%20-%20%5BSP-02%5D.png)
![Modelo Físico 1](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/Modelo%20F%C3%ADsico%20-%201%20%5BSP%20-%2002%5D.png)
![Modelo Físico 2](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/Modelo%20F%C3%ADsico%20-%202%20%5BSP%20-%2002%5D.png)
![Modelo Físico 3](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/Modelo%20F%C3%ADsico%20-%203%20%5BSP%20-%2002%5D.png)
![Modelo Físico 4](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/Modelo%20F%C3%ADsico%20-%204%20%5BSP%20-%2002%5D.png)
  
→ [Voltar ao topo](#topo)
  
<br>
</br>  
  
<span id="rotasfront">
<b> Rotas de Python e Frontend </b>
<p></p> 
  
 ![Rotas Python Administrador 1](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/adm%2001%20-%20rotas%20python.png)
 ![Rotas Python Administrador 2](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/adm%2002%20-%20rotas%20python.png)
 ![Rotas Python Administrador con](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/adm%20con%20-%20rotas%20python.png)
 ![Rotas Python alteração de dados](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/Alt%20dados_cli%20-%20rotas%20python.png) 
 ![Gráfico uso de Java Script 1](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/grafico%2001%20-%20rotas%20python.png)
 ![Gráfico uso de Java Script 2](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/grafico%2002%20-%20rotas%20python.png)
 ![CSS](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/css.png)
 ![HTML](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/html.png)
   
 → [Voltar ao topo](#topo)
  
<br>
</br> 
  
<span id="metequipe">
<b> Métricas da Equipe </b>
<p></p> 
<p align="justify">As atividades executadas para conclusão das entregas de valor para a Sprint 2 foram divididas por equipes internasda Impulse Team. A dupla Ryan Alves e Julio Lucena foi responsável pelo Banco de Dados. A dupla Naiara Leonor e Julio de Paula ficou com o frontend, desenvolvendo os templates HTML. Enquanto Gustavo Messa ficou responsável pelas rotas do Python e link entre HTML e Banco de Dados. 
Apesar da divisão em duplas, a medida que Gustavo necessitava, o restante do grupo colaborava também com a criação das rotas. A medida que as atividades de Banco de Dados e Templates foram finalizadas, todos os membros da equipe focaram na colaboração com o colega Gustavo Messa para conclusão do que a equipe identificou como maior desafio do projeto, que é a persistência de dados. Os dados de monitoramente de dedicação as atividades corroboram a visão da equipe e evidenciam a alta quantidade de horas dedicadas para o alcance da meta estabelecida pelo cliente. 
  
<br></br>  

![Gráfico Burndown e tabela de atividades](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/metricas%20da%20equipe%201%20-%20Impulse%20Team%20-%202022-1.png)  
![Tabela atividades metodologia](https://github.com/impulseteam/projeto-integrador-2022-1---FATEC-DSM/blob/main/planejamento/sprint-2/metricas%20da%20equipe%202%20-%20Impulse%20Team%20-%202022-1.png)   
  
→ [Voltar ao topo](#topo)
  
<br>
</br>
  
  
<span id="apfinal">
🏁 <b>Apresentação Sprint 2</b>
<p align="justify">Segue link para assistir a apresentação do que foi executado do projeto até o momento final da Sprint 2.</p> 
<p align="justify">Acesse: https://www.youtube.com/watch?v=89GHXYmHu7E </p>  
<br></br>

→ [Voltar ao topo](#topo)
  
<br>
</br>
