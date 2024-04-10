#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 22:37:49 2024

@author: andre
"""

import dash 
import dash_bootstrap_components as dbc

from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager, UserMixin
import sqlite3

import os

from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash

diretory = 'conteudos/3a'
path_db = 'data_3A.sqlite'

key_crypt = Fernet.generate_key()
cipher_suite = Fernet(key_crypt)
   
conn = sqlite3.connect(f'{path_db}')
engine = create_engine(f'sqlite:///{path_db}')
db = SQLAlchemy()

 
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    #email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(180))
    
Users_table = Table('users', Users.metadata)  

  
#def create_users_table():
#    Users.metadata.create_all(engine)

#create_users_table()

# Inicializa o SQLAlchemy com o aplicativo Flask
def init_app(app):
    db.init_app(app)

estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", dbc.themes.DARKLY]
dbc_css = "https://kit.fontawesome.com/a076d05399.js" 

app = dash.Dash(__name__)#,external_stylesheets=[dbc.themes.DARKLY])# external_stylesheets=[dbc.themes.DARKLY])#estilos)

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

# hashed_password = generate_password_hash('@Ndertron123', method='pbkdf2:sha256')
# ins = Users_table.insert().values(username='admin', password=hashed_password)
# conn = engine.connect()
# conn.execute(ins)
# conn.commit()
# conn.close()