from flask_mysqldb import MySQL
from flask import Flask
try:
    from backend import db_config as db
    from backend import db_classes as c
except:
    import db_config as db
    import db_classes as c
    
app = Flask(__name__)
app.config['MYSQL_USER'] = db.user
app.config['MYSQL_PASSWORD'] = db.password
app.config['MYSQL_DB'] = db.db
app.config['MYSQL_HOST'] = db.host
mysql = MySQL(app)

def criar_lista_cliente(resultado):
    lista_clientes = []
    for i in resultado:
        lista_clientes.append(c.Cliente(id_cliente=str(i[0])))
    return lista_clientes

def pesquisar_cliente(cpf='', cnpj=''):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('select * from cliente where cpf = %s and cnpj = %s', (cpf, cnpj))
    resultado = cursor.fetchall()
    cursor.close()
    if len(resultado)>0:
        return criar_lista_cliente(resultado)
    else:
        return []

def criar_lista_veiculo(resultado):
    lista_veiculos = []
    for i in resultado:
        lista_veiculos.append(c.Veiculo(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))
    return lista_veiculos

def pesquisar_veiculo(placa,chassi):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('select * from veiculo where placa = %s or chassi = %s', (placa, chassi))
    resultado = cursor.fetchall()
    cursor.close()
    if len(resultado)>0:
        return criar_lista_veiculo(resultado)
    else:
        return []

def pesquisar_cliente_geral(parametro):
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cliente WHERE lower(nome) LIKE %s OR lower(email) LIKE %s OR telefone LIKE %s OR cpf LIKE %s OR cnpj LIKE %s', (f"%{parametro.lower()}%", f"%{parametro.lower()}%", f"%{parametro.lower()}%", f"%{parametro.lower()}%", f"%{parametro.lower()}%"))
        resultado = cursor.fetchall()
        cursor.close()
        if len(resultado)>0:
            return criar_lista_cliente(resultado)
        else:
            return []
    except:
        return Exception
    
def pesquisar_veiculo_geral(parametro):
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM veiculo WHERE lower(id_veiculo) LIKE %s OR lower(placa) LIKE %s OR lower(chassi) LIKE %s OR id_cliente LIKE %s', (f"%{parametro.lower()}%", f"%{parametro.lower()}%", f"%{parametro.lower()}%", f"%{parametro.lower()}%"))
        resultado = cursor.fetchall()
        cursor.close()
        if len(resultado)>0:
            return criar_lista_veiculo(resultado)
        else:
            return []
    except:
        return Exception