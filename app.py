#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 22:37:49 2024

@author: andre
"""

import dash 
import dash_bootstrap_components as dbc

from sqlalchemy import Table, create_engine, MetaData
#from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager, UserMixin
import sqlite3
import socket
import pandas as pd

import os
from cryptography.fernet import Fernet
#from werkzeug.security import generate_password_hash

def get_ipv4_address():
    # Cria um socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Conecta-se a um servidor (neste caso, o Google DNS) para obter o endereço IP
        s.connect(('8.8.8.8', 80))
        # Obtém o endereço IPv4 atribuído ao socket
        ipv4_address = s.getsockname()[0]
    except Exception as e:
        #print("Ocorreu um erro ao obter o endereço IPv4:", e)
        ipv4_address = 'localhost'
        pass
    finally:
        # Fecha o socket
        s.close()
    return ipv4_address

#Configurações de execução para uma turma especifica
turma = '3A'
diretory = 'conteudos'#'\\3a'
path_db = 'databases\\users.sqlite'
link_server_local = 'http://{get_ipv4_address()}:8080'

key_crypt = Fernet.generate_key();
cipher_suite = Fernet(key_crypt)
   
conn = sqlite3.connect(f'{path_db}')
engine = create_engine(f'sqlite:///{path_db}')


db = SQLAlchemy()

# class Users(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     password = db.Column(db.String(180))

class Turmas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turma = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.String(255))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(180), nullable=False)
    
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'))
    # Relacionamento com a tabela Turmas
    turma = db.relationship('Turmas', backref=db.backref('users', lazy=True))    

turma_table = Table('turmas', Turmas.metadata)
Users_table = Table('users', Users.metadata)   


# Inicializa o SQLAlchemy com o aplicativo Flask
def init_app(app):
    db.init_app(app)

#estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", dbc.themes.DARKLY]
#dbc_css = "https://kit.fontawesome.com/a076d05399.js" 

app = dash.Dash(__name__)#, external_scripts=['asset'])#,external_stylesheets=[dbc.themes.BOOTSTRAP])# external_stylesheets=[dbc.themes.DARKLY])#estilos)

app.config['suppress_callback_exceptions'] = True
app.scripts.config.serve_locally = True
server = app.server 

server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{path_db}',
    SQLALCHEMY_TRACK_MODIFICATIONS=False)

db.init_app(server)

# Cria todas as tabelas definidas nos modelos se elas ainda não existirem no banco de dados
#if not os.path.exists('data.sqlite'):
# Users.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
