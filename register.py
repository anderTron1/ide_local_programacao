from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import *
from dash.exceptions import PreventUpdate

from dash import dash_table

from werkzeug.security import generate_password_hash

import numpy as np
import pandas as pd

card_style = {
    'width': '400px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
    'align-self': 'center'
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


def render_layout(message):
    conn1 = sqlite3.connect(path_db)
    df = pd.read_sql('SELECT * FROM users', conn1)
    df = df.drop(columns=['password'])
    df = df[['id', 'username']]
    conn1.close()
    
    message = "Ocorreu um erro durante o registro" if message == "error" else message
    register = html.Div([
            #dcc.State('df_today_users', data=df.to_dict('records')),
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.Row(html.Legend('Registros'), style={'display': 'flex', 'justify-content': 'center'}),
                            dbc.Row([
                                dbc.Input(id='user-register', placeholder='Username', type='text', style=input_style),
                                #dbc.Input(id='email-register', placeholder='E-mail', type='text'),
                                dbc.Input(id='pwd-register', placeholder='Password', type='password', style=input_style)
                            ], style={'display': 'flex', 'justify-content': 'center'}),
                            dbc.Row([
                                dbc.Col(dbc.Button('Salvar', id='register-button', style=button_style)),
                                dbc.Col(dbc.Button('Deletar', id='delete-register-button', style=button_style_cancel))
                            ], style={'display': 'flex', 'justify-content': 'center'}),
                            html.Span(message, style={'text-align': 'center'}),
                            html.Div([
                                html.Label('ou', style={'margin-right': '5px'}),
                                dcc.Link('Faça login', href='/login')
                            ], style={'padding': '20px', 'justify-content': 'center', 'display': 'flex'}),
                            html.Div(id='clicka')
                        
                        ], style=card_style)
                    ]),
                    dbc.Col([
                        dbc.Card([
                            dbc.Row([
                                html.B('Lista de Usuarios')
                            ]),
                            dbc.Row([
                                dash_table.DataTable(
                                    id='tabela-usuarios',
                                    columns=[{'name': col, 'id': col} for col in df.columns],
                                    data=df.to_dict('records'),
                                    editable=True,
                                    row_selectable="single",
                                    selected_rows=[],
                                )
                            ], style={'height': '300px', 'overflowY': 'auto'})
                        ])
                    ])
                ])
            ])
    ], style={'height': '100vh', 'display': 'flex', 'justify-content': 'center'})
    
    return register


@app.callback(
    Output('register-state', 'data'),
    #Output('tabela-usuarios', 'data'),
    Input('register-button', 'n_clicks'),
    Input('delete-register-button', 'n_clicks'),
    [
     State('user-register', 'value'),
     State('pwd-register', 'value'),
     #State('email-register', 'value'),
     State('tabela-usuarios','selected_rows'),
     State('tabela-usuarios', 'data'),
     ],
    #prevent_initial_call=True,
)
def register(n_clicks_register, n_clicks_delete, username, password, selected_rows, registers):
    if n_clicks_register:
        if username is not None and password is not None:
            if selected_rows == []:
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
                ins = Users_table.insert().values(username=username, password=hashed_password)
                conn = engine.connect()
        
                conn.execute(ins)
                conn.commit()
                conn.close()
            else:
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                
                id_edit = int(registers[selected_rows[0]]['id'])
                user_to_update = session.query(Users).filter_by(id=id_edit).first() 
                
                user_to_update.username = username
                user_to_update.password = hashed_password
                
                session.commit()
                
                return "continua"#, df
            
            return "continua"#, registers
        else:
            return "error"#, registers
        
    if n_clicks_delete:
        if selected_rows:
            id_edit = int(registers[selected_rows[0]]['id'])
            user_to_delete = session.query(Users).filter_by(id=id_edit).first() 
            
            session.delete(user_to_delete)
            session.commit()
            
            return 'continua'
            
    raise PreventUpdate

@app.callback(
    #Output('tabela-usuarios', 'data'),
    Output('user-register', 'value'),
    #Output('email-register', 'value'),
    Output('pwd-register', 'value'),
    Input('tabela-usuarios','selected_rows'),
    State('tabela-usuarios', 'data'),
    prevent_initial_call=True
)
def edit(selected_rows, registers):
    if selected_rows:
        user = registers[selected_rows[0]]['username']
        #email = registers[selected_rows[0]]['email']
        
        return user, ''
    raise PreventUpdate
    
# @app.callback(
#     Output('tabela-usuarios', 'data'),
    
#     Input('tabela-usuarios','selected_rows'),
    
#  )
    
# session.query(Users).filter_by(id=1).first() 
    
    
    
    
    
    
    
    