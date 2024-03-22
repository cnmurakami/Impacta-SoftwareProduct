from flask import Flask, render_template, request
import requests
from flask_mysqldb import MySQL
from backend import db_classes as c

#global variables
page_index = 'home'
page_customer_registration = 'register'
page_customer_search = 'customerSearch'
page_vehicle_registation = 'vehicle_registration'

app = Flask(__name__)
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Unitario123"
app.config['MYSQL_DB'] = "rscarautomotive"
# !!! Comente a linha abaixo caso esteja testando localmente !!!
app.config['MYSQL_HOST'] = 'db' 
mysql = MySQL(app)

def pesquisar_cliente(cpf, cnpj):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('select * from cliente where cpf = %s or cnpj = %s', (cpf, cnpj))
    result = cursor.fetchall()
    cursor.close()
    return result

@app.route('/', methods=['GET'])
def home():
    return render_template(f'{page_index}.html')

@app.route(f'/{page_customer_registration}', methods=['GET','POST'])
def register_customer():
    status_code=599
    if request.method == 'GET':
        return render_template(f'{page_customer_registration}.html')
    try:
        client_name = request.form['clientName']
        cpf = request.form['CPF']
        razao_social = request.form['RazaoSocial']
        cnpj = request.form['CNPJ']
        telefone = request.form['Telephone']
        celular = request.form['Cellphone']
        email1 = request.form['Email1']
        email2 = request.form['Email2']
        cep = request.form['CEP']
        logradouro = request.form['Logradouro']
        numero = request.form['Numero']
        complemento = request.form['Complemento']
        estado = request.form['brazilianStates']
        cidade = request.form['city']
        endereco = f'{logradouro}, {numero}, {complemento}, {cidade} - {estado}, CEP {cep}'
        if ((client_name and cpf) or (razao_social and cnpj)) and (telefone or celular) and (email1 or email2) and cep:
            status_code=550
            cliente_encontrado = pesquisar_cliente(cpf,cnpj)
            if (len(cliente_encontrado)>0):
                status_code=450
                raise
            else:
                status_code=551
                conn = mysql.connection
                cursor = conn.cursor()
                arg = (cpf, cnpj, client_name, razao_social, endereco, telefone, email1)
                cursor.callproc('inserir_cliente', arg)
                #cursor.execute('insert into cliente (cpf, cnpj, nome, razao_social, endereco, telefone, email) VALUES (%s, %s, %s, %s, %s, %s, %s)', (CPF, CNPJ, clientName, RazaoSocial, (f'{Logradouro}, {Numero}, {Complemento}, {city} - {brazilianStates}, CEP {CEP}'), (f'{Telephone}/{Cellphone}'), Email1))
                cursor.close()
                conn.commit()
            return render_template(f'{page_vehicle_registation}.html'), 200
        else:
            status_code=460
            raise
    except:
        return render_template(f'{page_customer_registration}.html'), status_code

#---WIP---
@app.route(f'/{page_customer_search}', methods = ['GET', 'POST'])
def search_customer():
    if request.method == 'GET':
        return render_template(f'{page_customer_search}')
    status_code = 599
    try:
        cpf = request.form['CPF']
        cnpj = request.form['CNPJ']
        if cpf or cnpj:
            status_code = status_code=550
            resultado = pesquisar_cliente(cpf,cnpj)
            if len(resultado)>0:
                return render_template (f'{page_customer_search}.html', cliente = resultado), 200
            else:
                status_code = 561
                raise
    except:
        return render_template(f'{page_customer_search}.html'), status_code


#---NOT IMPLEMENTED---
@app.route(f'/{page_vehicle_registation}', methods=['GET','POST'])
def vehicleregistration():
    return render_template(f'{page_vehicle_registation}.html', 501)

@app.route('/order', methods=['GET','POST'])
def placeorder():
    return render_template('order.html', 501)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)