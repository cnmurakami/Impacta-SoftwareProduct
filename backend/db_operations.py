from flask_mysqldb import MySQL
from flask import Flask, current_app
from backend import db_config as db
from backend import db_classes as c
import server as server


mysql = server.mysql


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
