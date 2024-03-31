from flask_mysqldb import MySQL
from flask import Flask
try: 
    from backend import db_config as db
except:
    import db_config as db

#import db_config as db

app = Flask(__name__)
app.config['MYSQL_USER'] = db.user
app.config['MYSQL_PASSWORD'] = db.password
app.config['MYSQL_DB'] = db.db
app.config['MYSQL_HOST'] = db.host
mysql = MySQL(app)

class Cliente:
    def __init__ (self, id_cliente:str = '', cpf:str = '', cnpj:str = '', nome:str = '', razao_social:str = '', endereco:str = '', telefone:str = '', email:str = ''):
        #lista completa: id_cliente, cpf, cnpj, nome, razao_social, endereco, telefone, email
        self.id_cliente = id_cliente
        self.cpf = cpf
        self.cnpj = cnpj
        self.nome = nome
        self.razao_social = razao_social
        self.endereco = endereco
        self.telefone = telefone
        self.email = email

    @property
    def id_cliente(self):
        return self._id_cliente
    
    @id_cliente.setter
    def id_cliente (self, novo_id_cliente):
        self._id_cliente = (novo_id_cliente)

        
    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def cpf (self, novo_cpf):
        self._cpf = (novo_cpf)

        
    @property
    def cnpj(self):
        return self._cnpj
    
    @cnpj.setter
    def cnpj (self, novo_cnpj):
        self._cnpj = (novo_cnpj)

        
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome (self, novo_nome):
        self._nome = (novo_nome)

        
    @property
    def razao_social(self):
        return self._razao_social
    
    @razao_social.setter
    def razao_social (self, novo_razao_social):
        self._razao_social = (novo_razao_social)

        
    @property
    def endereco(self):
        return self._endereco
    
    @endereco.setter
    def endereco (self, novo_endereco):
        self._endereco = (novo_endereco)

        
    @property
    def telefone(self):
        return self._telefone
    
    @telefone.setter
    def telefone (self, novo_telefone):
        self._telefone = (novo_telefone)

        
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email (self, novo_email):
        self._email = (novo_email)
    
    def endereco_completo(self):
        #'MeuLogradouro;;000;;MeuComplmento;;MinhaCidade;;SP;;01001-000'
        logradouro, numero, complemento, cidade, estado, cep = self.endereco.split(';;')
        return {'logradouro':logradouro, 'numero':numero, 'complemento':complemento, 'cidade':cidade, 'estado':estado, 'cep':cep}
    
    def insert(self):
        try:
            conn = mysql.connection
            cursor = conn.cursor()
            arg = (self.cpf, self.cnpj, self.nome, self.razao_social, self.endereco, self.telefone, self.email)
            cursor.callproc('inserir_cliente', arg)
            cursor.close()
            conn.commit()
        except:
            print ('ERRO NO INSERT')
            return Exception
    
    def send(self):
        info = {}
        info['id_cliente'] = self.id_cliente
        info['cpf'] = self.cpf
        info['cnpj'] = self.cnpj
        info['nome'] = self.nome
        info['razao_social'] = self.razao_social
        info.update(self.endereco_completo())
        info['telefone'] = self.telefone
        info['email'] = self.email
        return info

# novo_cliente = Cliente(id_cliente ='0', cpf ='123', cnpj ='456', nome ='aaaa', razao_social ='bbbb', endereco ='MeuLogradouro;;000;;MeuComplmento;;MinhaCidade;;SP;;01001-000', telefone ='0000', email = 'aaa@aaa.com')
# print (novo_cliente.send())
