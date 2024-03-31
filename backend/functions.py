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

def incluir_resultados(resultado):
    lista_clientes = []
    for i in resultado:
        lista_clientes.append(c.Cliente(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))
    return lista_clientes

def pesquisar_cliente(cpf='', cnpj=''):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('select * from cliente where cpf = %s and cnpj = %s', (cpf, cnpj))
    resultado = cursor.fetchall()
    cursor.close()
    if len(resultado)>0:
        return incluir_resultados(resultado)
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
            return incluir_resultados(resultado)
            #search_results.append({'clientname':row[3], 'cpf':row[1], 'cnpj':row[2], 'email1':row[7], 'cellphone':row[6]})
        else:
            return []
    except:
        return Exception