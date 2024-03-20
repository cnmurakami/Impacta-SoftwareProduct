from flask import Flask, render_template, request
import requests
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Unitario123"
app.config['MYSQL_DB'] = "rscarautomotive"
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    status_code=599
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
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('select * from cliente where cpf = %s or cnpj = %s', (cpf, cnpj))
            result = cursor.fetchall()
            cursor.close()
            if (len(result)>0):
                status_code=450
                raise
            else:
                status_code=551
                cursor = conn.cursor()
                arg=(cpf, cnpj, client_name, razao_social, endereco, telefone, email1)
                cursor.callproc('inserir_cliente',arg)
                #cursor.execute('insert into cliente (cpf, cnpj, nome, razao_social, endereco, telefone, email) VALUES (%s, %s, %s, %s, %s, %s, %s)', (CPF, CNPJ, clientName, RazaoSocial, (f'{Logradouro}, {Numero}, {Complemento}, {city} - {brazilianStates}, CEP {CEP}'), (f'{Telephone}/{Cellphone}'), Email1))
                cursor.close()
                conn.commit()
            return render_template('vehicle_registration.html'), 200
        else:
            status_code=460
            raise
    except:
        return render_template('register.html'), status_code

@app.route('/vehicleregistration', methods=['GET','POST'])
def vehicleregistration():
    return render_template('vehicle_registration.html')

@app.route('/order', methods=['GET','POST'])
def placeorder():
    return render_template('order.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)