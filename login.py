import os
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, State, Output
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user
from dash.exceptions import PreventUpdate
import pandas as pd
from sqlalchemy import select

from app import *


div_center_style = {
    'display': 'flex',
    'flexDirection': 'column',
    'alignItems': 'center',
    'justifyContent': 'center',
    'height': '100vh',  # Faz o conteúdo ocupar toda a altura da tela
    'margin': '-12px'
}

input_style = {
    'margin': '5px',
    'padding': '10px',
    'width': '300px',
    'borderRadius': '5px',
    'border': '1px solid #ccc'
}

button_style = {
    'margin': '5px',
    'padding': '10px',
    'width': '320px',
    'borderRadius': '5px',
    'backgroundColor': '#4CAF50',
    'color': 'white',
    'border': 'none',
    'cursor': 'pointer'
}

error_style = {
    'margin': '5px',
    'color': 'red'
}
conn1 = sqlite3.connect(f'{path_db}')
turmas = pd.read_sql("SELECT * FROM turmas", conn1)
conn1.close()

layout = html.Div(className='login', style=div_center_style, children=[
    #html.H2(f'Tela de Login turma: {turma}'),
    dcc.Input(id='username-input', type='text', placeholder='Usuário', style=input_style),
    dcc.Input(id='password-input', type='password', placeholder='Senha', style=input_style),
    dcc.Dropdown(
        id='tabela-dropdown',
        #options=[{'label': tabela, 'value': tabela} for tabela in turmas['turma']],
        options=[{'label': tabela['turma'], 'value': tabela['id']} for index, tabela in turmas.iterrows()],
        placeholder="Selecione a turma",
        style={'width': '320px', 'margin-top':'2px'}
    ),
    html.Button('Entrar', id='login-button', n_clicks=0, style=button_style),
    dcc.Interval(
        id='interval-login-msg', 
        interval=3000,  # Intervalo de 2 segundos
        n_intervals=1
    ),
    html.Div(id='login-status', style=error_style)
])

@app.callback(
    Output('rotas-url', 'data'),
    Output('login-status', 'children'),
    Input('store-login-status', 'data'),
    prevent_initial_call=True
)
def status_login(status):
    if status == "error-login":
        return  "", 'Usuário ou senha incorretos.'
    elif status == "error-class":
        return  "", 'Informe a turma.'
    else:
        return status, ""
    
    raise PreventUpdate

@app.callback(
    Output('login-status', 'style'),
    [Input('store-login-status', 'data'),
     Input('interval-login-msg', 'n_intervals'),
     #Input('interval-close-msg', 'n_intervals')
     ],
    prevent_initial_call=True
)
def display_message(btn_clicked, n_intervals):
    ctx = dash.callback_context
    if ctx.triggered_id == 'store-login-status':
        return {'display': 'block',  'color': 'red'}  # Exibe a mensagem quando o botão é clicado

    if n_intervals > 2:
        return {'display': 'none'}  # Oculta a mensagem após 2 segundos


@app.callback(
    Output('store-login-status', 'data'),
    #Output('table-selected', 'data'),
    Input('login-button', 'n_clicks'),
    State('username-input', 'value'),
    State('password-input', 'value'),
    State('tabela-dropdown', 'value'),
    State('tabela-dropdown', 'options'),
    prevent_initial_call=True
)
def check_login(n_clicks, username, password, tabled_id, tabled_selected):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    if n_clicks and changed_id == 'login-button.n_clicks':
        
        if username != "admin" and tabled_id == None:
            return "error-class"
        elif username != "admin":
            dir_path = None
            turma = [item["label"] for item in tabled_selected if item["value"] == tabled_id]
            for root, dirs, files in os.walk(diretory+'/'+turma[0]):
                if username in dirs:
                   path = os.path.abspath(os.path.join(root, username))
                   dir_path = username
            
        with app.server.app_context():
            if username != "admin":
                user = session.query(Users).filter_by(username=username, turma_id=tabled_id).first()
            else:
                user = session.query(Users).filter_by(username=username).first()
                
            if user is not None and password is not None:
                if check_password_hash(user.password, password):
                    login_user(user)
                    #password_cript = cipher_suite.encrypt(password.encode())
                    #email = current_user.email
                    
                    if current_user.username == 'admin':
                        return '/register'#, tables
                    elif username == dir_path:
                        return'/ide'#, ""
                else:
                      return "error-login"#, ""
        # with app.server.app_context():
        #         conn1 = sqlite3.connect(f'{path_db}')
        #         df = pd.read_sql(f"SELECT * FROM '{tables}' WHERE username='{username}'", conn1)
        #         df['database'] = tables
        #         user = df.iloc[0]
        #         conn1.close()
                
        #         if user is not None and password is not None: 
        #                 if check_password_hash(user['password'], password):
        #                     login_user(User(user)) 
        #                     #password_cript = cipher_suite.encrypt(password.encode())
        #                     #email = current_user.email
        #                     if current_user.username == 'admin':
        #                         print('administrador')
        #                         return '/register'
        #                     elif username == dir_path:
        #                         return'/ide'
        #                 else:
        #                       return "error"

    raise PreventUpdate


