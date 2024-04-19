import os
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, State, Output
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user
from dash.exceptions import PreventUpdate

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

layout = html.Div(className='login', style=div_center_style, children=[
    html.H2(f'Tela de Login turma: {turma}'),
    dcc.Input(id='username-input', type='text', placeholder='Usuário', style=input_style),
    dcc.Input(id='password-input', type='password', placeholder='Senha', style=input_style),
    html.Button('Entrar', id='login-button', n_clicks=0, style=button_style),
    html.Div(id='login-status', style=error_style)
])

@app.callback(
    Output('rotas-url', 'data'),
    Output('login-status', 'children'),
    Input('store-login-status', 'data'),
    prevent_initial_call=True
)
def status_login(status):
    if status == "error":
        return  "", html.Div('Usuário ou senha incorretos.', style={'color': 'red'})
    else:
        return status, ""
    
    raise PreventUpdate

@app.callback(
    Output('store-login-status', 'data'),
    Input('login-button', 'n_clicks'),
    State('username-input', 'value'),
    State('password-input', 'value'),
    prevent_initial_call=True
)
def check_login(n_clicks, username, password):
    if n_clicks == None:
        raise PreventUpdate
        
    dir_path = None
    for root, dirs, files in os.walk(diretory):
        if username in dirs:
           path = os.path.abspath(os.path.join(root, username))
           dir_path = username
        
    with app.server.app_context():
        user = session.query(Users).filter_by(username=username).first()
        
        if user is not None and password is not None:
            if check_password_hash(user.password, password):
                login_user(user)
                #password_cript = cipher_suite.encrypt(password.encode())
                #email = current_user.email
                
                if current_user.username == 'admin':
                    return '/register'
                elif username == dir_path:
                    return'/ide'
            else:
                 return "error"
    raise PreventUpdate


