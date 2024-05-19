from flask_mysqldb import MySQL
from flask import Flask
from abc import ABC
from backend import db_operations as db

class Rscar(ABC):
    def enviar(self):
        return ''
    def salvar(self):
        return ''

class Cliente(Rscar):
    #id_cliente, cpf, cnpj, nome, razao_social, endereco, telefone, email
    def __init__ (self, id_cliente:str = '', cpf:str = '', cnpj:str = '', nome:str = '', razao_social:str = '', endereco:str = '', telefone:str = '', email:str = ''):
        if id_cliente != '':
            resultado = db.execute('select * from cliente where id_cliente = %s', (id_cliente,))
            if len(resultado) == 1:
                self.id_cliente = id_cliente
                self.cpf = resultado[0][1]
                self.cnpj = resultado[0][2]
                self.nome = resultado[0][3]
                self.razao_social = resultado[0][4]
                self.endereco = resultado[0][5]
                self.telefone = resultado[0][6]
                self.email = resultado[0][7]
            else:
                raise Exception
        else:
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
        self._id_cliente = novo_id_cliente

    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def cpf (self, novo_cpf):
        self._cpf = novo_cpf
  
    @property
    def cnpj(self):
        return self._cnpj
    
    @cnpj.setter
    def cnpj (self, novo_cnpj):
        self._cnpj = novo_cnpj

    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome (self, novo_nome):
        self._nome = novo_nome

    @property
    def razao_social(self):
        return self._razao_social
    
    @razao_social.setter
    def razao_social (self, novo_razao_social):
        self._razao_social = novo_razao_social
        
    @property
    def endereco(self):
        return self._endereco
    
    @endereco.setter
    def endereco (self, novo_endereco):
        self._endereco = novo_endereco

    @property
    def telefone(self):
        return self._telefone
    
    @telefone.setter
    def telefone (self, novo_telefone):
        self._telefone = novo_telefone

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email (self, novo_email):
        self._email = novo_email
    
    def endereco_completo(self):
        #'MeuLogradouro;;000;;MeuComplmento;;MinhaCidade;;SP;;01001-000'
        try:
            logradouro, numero, complemento, cidade, estado, cep = self.endereco.split(';;')
            return {'logradouro':logradouro, 'numero':numero, 'complemento':complemento, 'cidade':cidade, 'estado':estado, 'cep':cep}
        except:
            return {'endereco':self.endereco}
    
    def salvar(self):
        try:
            db.procedure('inserir_cliente', (self.cpf, self.cnpj, self.nome, self.razao_social, self.endereco, self.telefone, self.email))
        except:
            print ('ERRO NO INSERT')
            raise Exception
    
    def enviar(self):
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

class Veiculo(Rscar):
    #id_veiculo, id_cliente, placa, chassi, marca, modelo, ano_fabricacao, ano_modelo, cor
    def __init__ (self, id_veiculo:str = '', id_cliente:str = '', placa:str = '', chassi:str = '', marca:str = '', modelo:str = '', ano_fabricacao:str = '', ano_modelo:str = '', cor:str = ''):
        #lista completa: id_veiculo, id_cliente, cpf, cnpj, nome, razao_social, endereco, telefone, email
        if id_veiculo != '':
            resultado = db.execute('select * from veiculo where id_veiculo = %s', (id_veiculo,))
            if len(resultado) == 1:
                self.id_veiculo = id_veiculo
                self.id_cliente = resultado[0][1]
                self.placa = resultado[0][2]
                self.chassi = resultado[0][3]
                self.marca = resultado[0][4]
                self.modelo = resultado[0][5]
                self.ano_fabricacao = resultado[0][6]
                self.ano_modelo = resultado[0][7]
                self.cor = resultado[0][8]
            else:
                raise
        else:
            self.id_veiculo = ''
            self.id_cliente = id_cliente
            self.placa = placa
            self.chassi = chassi
            self.marca = marca
            self.modelo = modelo
            self.ano_fabricacao = ano_fabricacao
            self.ano_modelo = ano_modelo
            self.cor = cor

    @property
    def id_veiculo(self):
        return self._id_veiculo

    @id_veiculo.setter
    def id_veiculo(self, novo_id_veiculo):
        self._id_veiculo = novo_id_veiculo
    

    @property
    def id_cliente(self):
        return self._id_cliente

    @id_cliente.setter
    def id_cliente(self, novo_id_cliente):
        self._id_cliente = novo_id_cliente
    

    @property
    def placa(self):
        return self._placa

    @placa.setter
    def placa(self, novo_placa):
        self._placa = novo_placa
    

    @property
    def chassi(self):
        return self._chassi

    @chassi.setter
    def chassi(self, novo_chassi):
        self._chassi = novo_chassi
    

    @property
    def marca(self):
        return self._marca

    @marca.setter
    def marca(self, novo_marca):
        self._marca = novo_marca
    

    @property
    def modelo(self):
        return self._modelo

    @modelo.setter
    def modelo(self, novo_modelo):
        self._modelo = novo_modelo
    

    @property
    def ano_fabricacao(self):
        return self._ano_fabricacao

    @ano_fabricacao.setter
    def ano_fabricacao(self, novo_ano_fabricacao):
        self._ano_fabricacao = novo_ano_fabricacao
    

    @property
    def ano_modelo(self):
        return self._ano_modelo

    @ano_modelo.setter
    def ano_modelo(self, novo_ano_modelo):
        self._ano_modelo = novo_ano_modelo
    

    @property
    def cor(self):
        return self._cor

    @cor.setter
    def cor(self, novo_cor):
        self._cor = novo_cor

    
    def salvar(self):
        try:
            db.procedure('inserir_veiculo', (self.id_cliente, self.placa, self.chassi, self.marca, self.modelo, self.ano_fabricacao, self.ano_modelo, self.cor))
        except:
            print ('ERRO NO INSERT')
            raise Exception
    
    def enviar(self):
        info = {}
        info['id_veiculo'] = self.id_veiculo
        info['id_cliente'] = self.id_cliente
        info['placa'] = self.placa
        info['chassi'] = self.chassi
        info['marca'] = self.marca
        info['modelo'] = self.modelo
        info['ano_fabricacao'] = self.ano_fabricacao
        info['ano_modelo'] = self.ano_modelo
        info['cor'] = self.cor
        return info
