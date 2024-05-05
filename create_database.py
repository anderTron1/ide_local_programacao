# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 11:21:23 2024

@author: user
"""
import sqlite3
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, create_engine, MetaData
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os
import sys

for i in range(len(sys.argv)):
    if sys.argv[i] == '-t':
        name_path = sys.argv[i+1]
        name_path = name_path.upper()
        break

diretory = 'conteudos'
diretory_support = 'apoio'
diretory_df = 'databases'

#Verificar se algumas pastas importantes existe, caso não cria elas
if not os.path.exists(f'{diretory}/{diretory_support}'):
    os.makedirs(f'{diretory}/{diretory_support}')
    
if not os.path.exists(diretory_df):
    os.makedirs(diretory_df)

#Carregando elementos do sqlite
conn = sqlite3.connect(f'{diretory_df}\\users.sqlite')
engine = create_engine(f'sqlite:///{diretory_df}\\users.sqlite')#data_{name_path}.sqlite')
db = SQLAlchemy()

class Turmas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turma = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.String(255))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(180), nullable=False)
    
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'))
    # Relacionamento com a tabela Turmas
    turma = db.relationship('Turmas', backref=db.backref('users', lazy=True))
    
turmas_table = Table('turmas', Turmas.metadata)
Users_table = Table('users', Users.metadata)#Table('users', Users.metadata)  

def create_users_table():
    Users.metadata.create_all(engine)

def create_turmas_table():
    Turmas.metadata.create_all(engine)

create_turmas_table()
create_users_table()

if not os.path.exists("{diretory_df}\\users.sqlite"):
    exist = True
        
if not exist:
    create_users_table()
    create_turmas_table()

if os.path.exists(diretory):
    os.makedirs(f"{os.path.abspath(diretory)}\\{name_path}")

Session = sessionmaker(bind=engine)
session = Session()

ins = turmas_table.insert().values(turma=name_path)
conn = engine.connect()
conn.execute(ins)
conn.commit()
conn.close()

#Criar um usuario e senha padrão de administrador 
hashed_password = generate_password_hash('123', method='pbkdf2:sha256')
ins = Users_table.insert().values(username='admin', password=hashed_password)
conn = engine.connect()
conn.execute(ins)
conn.commit()
conn.close()
