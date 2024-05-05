from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import *
from dash.exceptions import PreventUpdate
from sqlalchemy.exc import IntegrityError
from dash import dash_table

from werkzeug.security import generate_password_hash

import numpy as np
import pandas as pd

import os

card_style = {
    'width': '400px',
    'min-height': '250px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
    'align-self': 'center',
    'border':'1px solid #ced4da'
}

button_style = {
    'margin': '5px',
    'padding': '10px',
    'width': '120px',
    'borderRadius': '5px',
    'backgroundColor': '#4CAF50',
    'color': 'white',
    'border': 'none',
    'cursor': 'pointer'
}

button_style_cancel = {
    'margin': '5px',
    'padding': '10px',
    'width': '120px',
    'borderRadius': '5px',
    'backgroundColor': '#FFA07A',
    'color': 'white',
    'border': 'none',
    'cursor': 'pointer'
}

input_style = {
    'margin': '5px',
    'padding': '10px',
    'width': '300px',
    'borderRadius': '5px',
    'border': '1px solid #ccc'
}

#card_style = {'margin': '20px', 'border': '1px solid #ced4da', 'border-radius': '5px'}

def render_layout(message, name_database='1B'):
    # conn1 = sqlite3.connect(path_db)
    # df = pd.read_sql(f"SELECT * FROM 'users'", conn1)
    # df = df.drop(columns=['password'])
    # df = df[['id', 'username']]
    # conn1.close()
    
    #message = "Ocorreu um erro durante o registro" if message == "error" else message
    register = dbc.Container([
            #dcc.State('df_today_users', data=df.to_dict('records')),
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            html.Legend('Registros'),

                            dbc.Input(id='user-register', placeholder='Username', type='text', style=input_style),
                                #dbc.Input(id='email-register', placeholder='E-mail', type='text'),
                            dbc.Input(id='pwd-register', placeholder='Password', type='password', style=input_style),
                            
                            dcc.Dropdown(
                                id='tabela-turmas-dropdown',
                                #options=[{'label': tabela, 'value': tabela} for tabela in turmas['turma']],
                                placeholder="Selecione a turma",
                                style={'width': '320px', 'margin-top':'2px'}
                            ),
                            
                            dbc.Row([
                                dbc.Col(dbc.Button('Salvar', id='register-button', style=button_style)),
                                dbc.Col(dbc.Button('Deletar', id='delete-register-button', style=button_style_cancel)),
                            ], style={'display': 'flex'}),
                            
                            dbc.Row([
                                dbc.Input(id="input-turma", placeholder="Nova Turma...", style=input_style),
                                dbc.Button('Salvar turma', id="save-turma", style=button_style)
                            ]),
                            dcc.Interval(
                                id='interval-register-msg', 
                                interval=4000,  # Intervalo de 2 segundos
                                n_intervals=1
                            ),
                            html.Span(id="msg-error-register", style={'text-align': 'center', 'color': 'red'}),
                            html.Div(id="msg-error-class", style={'text-align': 'center', 'color': 'red'}),
                            html.Div([
                                html.Label('ou', style={'margin-right': '5px'}),
                                dcc.Link('Faça login', href='/login')
                            ], style={'padding': '20px', 'justify-content': 'center', 'display': 'flex'}),
                            html.Div(id='clicka')
                        
                        ], style=card_style)
                    ], md=4),
                    dbc.Col([
                            dbc.Card([
                                dbc.Row([
                                    html.B('Lista de Usuarios')
                                ]),
                                dbc.Row(id='table-users',
                                    children=[#dash_table.DataTable(id='tabela-usuarios')
                                    dash_table.DataTable(
                                        id='tabela-usuarios',
                                        columns=[{'name': col, 'id': col} for col in ['id', 'username', 'turma_id']],
                                        #data=df.to_dict('records'),
                                        editable=True,
                                        row_selectable="single",
                                        selected_rows=[],
                                    )
                                    ], 
                                    style={'height': '260px', 'overflowY': 'auto', 'width': '20vw'}),
                            ], style={'padding-left': '10px'})
                    ], md=4, style={'border':'1px solid #ced4da'}),
                    dbc.Col([
                        dbc.Row([
                            html.B('Lista de Turmas')
                        ]),
                        dbc.Row([
                                dash_table.DataTable(
                                    id='tabela-turmas',
                                    columns=[{'name': col, 'id': col} for col in ['id', 'turma']],
                                    #data=df.to_dict('records'),
                                    editable=True,
                                    row_selectable="single",
                                    selected_rows=[],
                                )
                            ],style={'height': '260px', 'overflowY': 'auto', 'width': '20vw'}
                        )
                    ], md=4, style={'border':'1px solid #ced4da'})
                ], style={'display': 'flex', 'justify-content': 'center'})
            ])
    ], fluid=True, style={"margin-top": '20vh'})#, style={'height': '100vh', 'display': 'flex', 'justify-content': 'center'})
    
    return register

@app.callback(
    #Output('tabela-usuarios', 'data'),
    Output('tabela-turmas-dropdown', 'options'),
    Output('tabela-turmas', 'data'),
    Input('url', 'pathname'),
    #[State('tabela-dropdown', 'value')],
    #prevent_initial_call=True,
)
def update_table_data(pathname):
    if pathname == '/register':
        conn1 = sqlite3.connect(path_db)
        # df = pd.read_sql(f"SELECT id, username, turma_id FROM users WHERE username='admin'", conn1)
        #conn1.close()
        
        #conn1 = sqlite3.connect(f'{path_db}')
        turmas = pd.read_sql("SELECT id, turma FROM turmas ORDER BY id", conn1)
        conn1.close()
        
        #return df.to_dict('records'),
        return [{'label': tabela['turma'], 'value': tabela['id']} for index, tabela in turmas.iterrows()], turmas.to_dict('records')
    raise PreventUpdate
    
@app.callback(
    Output('tabela-usuarios', 'data'),
    Input('tabela-turmas', 'selected_rows'),
    Input('url', 'pathname'),
    State('tabela-turmas', 'data'),
    #prevent_initial_call=True
)
def update_table_user(selected_rows, pathname, df_turma):
    if selected_rows != None and selected_rows != []:
       id = df_turma[selected_rows[0]]['id']
       conn1 = sqlite3.connect(path_db)
       df = pd.read_sql(f"SELECT id, username, turma_id FROM users WHERE (turma_id={int(id)} OR username='admin') ORDER BY username", conn1)
       conn1.close()
       
       return df.to_dict('records')
    
    if pathname == '/register':
        conn1 = sqlite3.connect(path_db)
        df = pd.read_sql(f"SELECT id, username, turma_id FROM users WHERE username='admin'", conn1)
        conn1.close()
        return df.to_dict('records')

@app.callback(
    Output('tabela-usuarios', 'selected_rows'),
    Input('tabela-turmas', 'selected_rows'),
    prevent_initial_call=True
)
def remove_selected_users(selected):
    if selected != None and selected != []:
        return []
    

@app.callback(
    Output('input-turma', 'value'),
    Input('tabela-turmas','selected_rows'),
    State('tabela-turmas', 'data')
)
def edit_turma(selected_rows, registers):
    if selected_rows:
        turma = registers[selected_rows[0]]['turma']
        return turma, 
    raise PreventUpdate
        

@app.callback(
    Output('register-state', 'data'),
    Input('register-button', 'n_clicks'),
    Input('delete-register-button', 'n_clicks'),
    [
     State('user-register', 'value'),
     State('pwd-register', 'value'), 
     State('tabela-usuarios','selected_rows'),
     State('tabela-usuarios', 'data'),
     State('tabela-turmas-dropdown', 'value'),
     State('tabela-turmas-dropdown', 'options')
     ],
    prevent_initial_call=True,
)
def register(n_clicks_register, n_clicks_delete, username, password, selected_rows, registers, select_id_turma, select_turma):
    if n_clicks_register:
        if username is not None and username is not ""  and password is not None and password is not "":
            if selected_rows == [] and select_id_turma is not None:
                turma = [item["label"] for item in select_turma if item["value"] == select_id_turma]
                if os.path.exists(diretory+'\\'+turma[0]+'\\'+username.upper()):
                    return 'user-exist'
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                    
                username = username.upper()
                ins = Users_table.insert().values(username=username, password=hashed_password, turma_id=select_id_turma)
                conn = engine.connect()
            
                conn.execute(ins)
                conn.commit()
                conn.close()
                    
                if os.path.exists(diretory+'\\'+turma[0]):
                    direct = diretory+'\\'+turma[0]
                    os.makedirs(f"{os.path.abspath(direct)}\\{username}\\imagens")
                return 'user-save'
            else:
                if select_id_turma == None and username != 'admin':
                    return "error"
                
                id_edit = int(registers[selected_rows[0]]['id'])
                user_to_update = session.query(Users).filter_by(id=id_edit).first() 
                    
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                
                if user_to_update.username == "admin":
                    if username != user_to_update.username:
                        return "error-admin"
                elif user_to_update.username != username:
                    turma = [item["label"] for item in select_turma if item["value"] == select_id_turma]
                    try:
                        path = diretory+'\\'+turma[0]+'\\'
                        if os.path.exists(path+user_to_update.username):
                            os.rename(path+user_to_update.username, path+username)
                    except OSError as e:
                        return 'error-rename-direct'
                user_to_update.username = username
                user_to_update.password = hashed_password
                
                # if user_to_update.username != "admin":
                #     user_to_update.turma_id = select_id_turma
                
                session.commit()
                
                return "user-changed"
        else:
            return "error"#, registers
        
    if n_clicks_delete:
        if selected_rows:
            id_edit = int(registers[selected_rows[0]]['id'])
            user_to_delete = session.query(Users).filter_by(id=id_edit).first() 
            
            if user_to_delete.username == 'admin':
                return "error-deleted"#, registers
            session.delete(user_to_delete)
            session.commit()

            return 'user-deleted'
            
    raise PreventUpdate
    
@app.callback(
    Output('msg-error-class', 'children'),
    Output('register-class-state', 'data'),
    Input('save-turma', 'n_clicks'),
    State('input-turma', 'value'),
    prevent_initial_call=True
)
def salve_class(btn_clicked, value_input_class):
    if btn_clicked:
        value_class = value_input_class.upper()
        
        if value_input_class != None and value_input_class != "":            
            try:
                ins = turma_table.insert().values(turma=value_class)
                conn = engine.connect()
        
                conn.execute(ins)
                conn.commit()
                conn.close()
            except IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    return f"Erro de violação de restrição: A turma {value_class} já existe!", 'error'
                else:
                    return "Erro de integridade no banco de dados", 'error'
            return 'Nova turma salvo', 'salvo'
        
    raise PreventUpdate
    
@app.callback(
    Output('user-register', 'value'),
    Output('tabela-turmas-dropdown', 'value'),
    Output('pwd-register', 'value'),
    Input('tabela-usuarios','selected_rows'),
    State('tabela-usuarios', 'data'),
    prevent_initial_call=True
)
def edit(selected_rows, registers):
    if selected_rows:
        user = registers[selected_rows[0]]['username']
        turma =  registers[selected_rows[0]]['turma_id']
        return user, turma, ''
    else:
        return "", "", ""
    raise PreventUpdate
    
@app.callback(
    Output('msg-error-register', 'children'),
    Input('register-state', 'data'),
    prevent_initial_call=True
)
def status_login(status):
    if status == "error-admin":
        return  'Nome do usuário administrador não pode ser alterado'
    elif status == "error":
        return  'Informe todos os dados'
    elif status == "user-save":
        return "Usuário salvo!"
    elif status == "user-changed":
        return "Usuário alterado!"
    elif status == "user-deleted":
        return "Usuário deletado!"
    elif status == "error-deleted":
        return "Usuário administrador não pode ser deletado"
    elif status == "user-exist":
        return "O usuário já existe!"
    elif status == "error-rename-direct":
        return "Erro ao modificar o nome do diretorio"
    else:
        return status, "Usuário alterado!"

    raise PreventUpdate

@app.callback(
    Output('msg-error-register', 'style'),
    [Input('register-state', 'data'),
     Input('interval-register-msg', 'n_intervals')],
    prevent_initial_call=True
)
def display_message(state, n_intervals):
    ctx = dash.callback_context
    if ctx.triggered_id == 'register-state':
        return {'display': 'block',  'color': 'red'}  # Exibe a mensagem quando o botão é clicado

    if n_intervals > 2:
        return {'display': 'none'}  # Oculta a mensagem após 2 segundos
    
    
@app.callback(
    Output('msg-error-class', 'style'),
    [Input('register-class-state', 'data'),
     Input('interval-register-msg', 'n_intervals')],
    prevent_initial_call=True
)
def display_message(state, n_intervals):
    ctx = dash.callback_context
    if ctx.triggered_id == 'register-class-state':
        return {'display': 'block',  'color': 'red'}  # Exibe a mensagem quando o botão é clicado

    if n_intervals > 2:
        return {'display': 'none'}  # Oculta a mensagem após 2 segundos
    
    
    
    
    
    
    