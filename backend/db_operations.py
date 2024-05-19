from flask_mysqldb import MySQL
from flask import Flask
from backend import db_config as db
from backend import db_classes as c

app = Flask(__name__)
app.config['MYSQL_USER'] = db.user
app.config['MYSQL_PASSWORD'] = db.password
app.config['MYSQL_DB'] = db.db
app.config['MYSQL_HOST'] = db.host
mysql = MySQL(app)

def procedure(proc_name:str, arg:tuple):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.callproc(proc_name, arg)
    cursor.close()
    conn.commit()
    return

def execute(query:str, arg:tuple):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(query, arg)
    resultado = cursor.fetchall()
    cursor.close()
    return resultado
