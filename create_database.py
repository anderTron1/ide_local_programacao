# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 11:21:23 2024

@author: user
"""

import sqlite3
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, create_engine
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os
import sys

for i in range(len(sys.argv)):
    if sys.argv[i] == '-d':
        name_path = sys.argv[i+1]
        name_path = name_path.upper()
        break

diretory = 'conteudos'
conn = sqlite3.connect(f'databases\\data_{name_path}.sqlite')
engine = create_engine(f'sqlite:///databases\\data_{name_path}.sqlite')
db = SQLAlchemy()

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(180))
    
Users_table = Table('users', Users.metadata)  

def create_users_table():
    Users.metadata.create_all(engine)

if not os.path.exists("databases\\data_{name_path}.sqlite"):
    create_users_table()

if os.path.exists(diretory):
    os.makedirs(f"{os.path.abspath(diretory)}\\{name_path}")

Session = sessionmaker(bind=engine)
session = Session()

hashed_password = generate_password_hash('123', method='pbkdf2:sha256')
ins = Users_table.insert().values(username='admin', password=hashed_password)
conn = engine.connect()
conn.execute(ins)
conn.commit()
conn.close()