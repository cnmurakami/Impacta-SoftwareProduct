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
    try:
        clientName = request.form['clientName']
        CPF = request.form['CPF']
        RazaoSocial = request.form['RazaoSocial']
        CNPJ = request.form['CNPJ']
        Telephone = request.form['Telephone']
        Cellphone = request.form['Cellphone']
        Email1 = request.form['Email1']
        Email2 = request.form['Email2']
        CEP = request.form['CEP']
        Logradouro = request.form['Logradouro']
        Numero = request.form['Numero']
        Complemento = request.form['Complemento']
        brazilianStates = request.form['brazilianStates']
        city = request.form['city']
        if ((clientName and CPF) or (RazaoSocial and CNPJ)) and (Telephone or Cellphone) and (Email1 or Email2) and CEP:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('insert into cliente (cpf, cnpj, nome, razao_social, endereco, telefone, email) VALUES (%s, %s, %s, %s, %s, %s, %s)', (CPF, CNPJ, clientName, RazaoSocial, (f'{Logradouro}, {Numero}, {Complemento}, {city} - {brazilianStates}, CEP {CEP}'), (f'{Telephone}/{Cellphone}'), Email1))
            conn.commit()
            return render_template('vehicle_registration.html')
    except:
        return render_template('register.html'),500

@app.route('/vehicleregistration', methods=['GET','POST'])
def vehicleregistration():
    return render_template('vehicle_registration.html')

@app.route('/order', methods=['GET','POST'])
def placeorder():
    return render_template('order.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)