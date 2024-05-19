from flask import Flask, render_template, request, url_for, redirect, jsonify
import requests
from flask_mysqldb import MySQL
from backend import functions as f
from backend import db_classes as c
from backend import db_config as db_config

#global variables
page_index = 'home'
page_customer_registration = 'register'
page_customer_search = 'search'
page_vehicle_registration = 'vehicle_registration'

app = Flask(__name__)
app.config['MYSQL_USER'] = db_config.user
app.config['MYSQL_PASSWORD'] = db_config.password
app.config['MYSQL_DB'] = db_config.db
app.config['MYSQL_HOST'] = db_config.host
mysql = MySQL(app)

@app.route('/', methods=['GET'])
def home():
    return render_template(f'{page_index}.html')

@app.route(f'/{page_customer_registration}/', methods=['GET','POST'])
def register():
    status_code=599
    if request.method == 'GET':
        return render_template(f'{page_customer_registration}.html')
    try:
        client_name = request.form['clientName']
        cpf = request.form['CPF']
        razao_social = request.form['RazaoSocial']
        cnpj = request.form['CNPJ']
        celular = request.form['Cellphone']
        email1 = request.form['Email1']
        cep = request.form['CEP']
        logradouro = request.form['Logradouro']
        numero = request.form['Numero']
        complemento = request.form['Complemento']
        estado = request.form['brazilianStates']
        cidade = request.form['city']
        telefone = celular
        endereco = f'{logradouro};;{numero};;{complemento};;{cidade};;{estado};;{cep}'
        if ((client_name and cpf) or (razao_social and cnpj)) and telefone and email1 and cep:
            status_code=550
            cliente_encontrado = f.pesquisar_cliente(cpf,cnpj)
            if (len(cliente_encontrado)>0):
                status_code=450
                raise
            else:
                status_code=551
                novo_cliente = c.Cliente(cpf=cpf, cnpj=cnpj, nome=client_name, razao_social = razao_social, endereco=endereco, telefone=telefone, email=email1)
                novo_cliente.salvar()
                try:
                    cliente_confirmado = f.pesquisar_cliente(cpf,cnpj)[0]
                    return render_template(f'{page_vehicle_registration}.html')
                except:
                    return render_template(f'{page_customer_registration}.html'), 552
        else:
            status_code=460
            raise
    except:
        return render_template(f'{page_customer_registration}.html'), status_code

@app.route(f'/get_last_client_data', methods = ['GET'])
def get_last_client_data():
    pass

@app.route(f'/search/', methods = ['GET'])
def search():
    return render_template(f'{page_customer_search}.html', search_results=[]), 200

@app.route(f'/searchdatabase/', methods = ['GET'])
def search_customer():
    try:
        pesquisa_cliente = request.args.get('procura')
        if pesquisa_cliente:
            search_results = []
            try:
                status_code = 550
                busca_clientes = f.pesquisar_cliente_geral(pesquisa_cliente)
                if len(busca_clientes)>0:
                    status_code = 200
                    try:
                        for cliente in busca_clientes:
                            search_results.append(cliente.enviar())
                    except:
                        status_code = 552
                else:
                    status_code = 561
            except:
                return render_template(f'{page_customer_search}.html'), status_code

            return render_template(f'{page_customer_search}.html', search_results=search_results), status_code
    except:
        return redirect(f'{page_customer_search}.html'), 460

@app.route(f'/searchdatabaseveiculo/', methods = ['GET'])
def search_vehicle():
    try:
        pesquisa_veiculo = request.args.get('procura_veiculo')
        if pesquisa_veiculo:
            search_results = []
            try:
                status_code = 550
                busca_veiculos = f.pesquisar_veiculo_geral(pesquisa_veiculo)
                if len(busca_veiculos)>0:
                    status_code = 200
                    try:
                        for veiculo in busca_veiculos:
                            search_results.append(veiculo.enviar())
                    except:
                        status_code = 552
                else:
                    status_code = 561
            except:
                return render_template(f'{page_customer_search}.html'), status_code

            return render_template(f'{page_customer_search}.html', search_results=search_results), status_code
    except:
        return redirect(f'{page_customer_search}.html'), 460
# @app.route(f'/cliente/<id_cliente>/', methods = ['GET'])
# def exibir_cliente(id_cliente):
#     status_code = 561
#     try:
#         cliente_atual = c.Cliente(id_cliente=id_cliente)
#         return render_template('cliente.html', cliente=cliente_atual.enviar())#, 200
#     except:
#         return render_template('cliente.html', cliente = {}), status_code

#---WIP---
# @app.route(f'/cliente/<id_cliente>/{page_vehicle_registration}/', methods=['GET','POST'])
# def vehicle_registration(id_cliente):
#     try:
#         status_code = 200
#         cliente_atual = c.Cliente(id_cliente=id_cliente)
#         cliente = cliente_atual.enviar()
#     except:
#         status_code = 561
#         cliente = {}
#     if request.method == 'GET':
#         return render_template (f'{page_vehicle_registration}.html', cliente = cliente), status_code
#     status_code = 200
#     try:
#         status_code = 561
#         status_code = 460
#         placa = request.form['placa']
#         chassi = request.form['chassi']
#         marca = request.form['marca']
#         modelo = request.form['modelo']
#         ano_fabricacao = request.form['ano_fabricacao']
#         ano_modelo = request.form['ano_modelo']
#         cor = request.form['cor']
#         status_code=550
#         if placa and chassi:
#             veiculo_encontrado = f.pesquisar_veiculo(placa,chassi)
#             if (len(veiculo_encontrado)>0):
#                 status_code=450
#                 raise
#             else:
#                 status_code=551
#                 novo_veiculo = c.Veiculo(id_cliente = cliente_atual.id_cliente, placa = placa, chassi = chassi, marca = marca, modelo = modelo, ano_fabricacao = ano_fabricacao, ano_modelo = ano_modelo, cor = cor)
#                 novo_veiculo.salvar()
#                 return render_template(f'{page_vehicle_registration}.html', cliente = cliente), 200
#         else:
#             status_code = 460
#             raise
#     except:
#         return render_template(f'{page_vehicle_registration}.html',cliente = cliente), status_code
@app.route(f'/{page_vehicle_registration}/')
def vehicle_registration():
    return render_template(f'{page_vehicle_registration}.html')

#---NOT IMPLEMENTED---
# @app.route('/order/', methods=['GET','POST'])
# def placeorder():
#     return render_template('order.html', 501)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)