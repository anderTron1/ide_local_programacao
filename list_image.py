import os
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, State, Output
from dash_bootstrap_components import Modal, ModalHeader, ModalBody, ModalFooter
from app import *
import asyncio
import aiohttp

def listar_pastas(diretorio):
    pastas = []
    # Obter todos os itens no diretório
    path = os.path.abspath(diretorio)
    itens = os.listdir(path)
    caminho_completo = []
    # Verificar cada item se é um diretório
    for item in itens:
        # Obter o caminho completo do item
        caminho_completo = os.path.join(diretorio, item)
        # Verificar se o item é um diretório
        if os.path.isdir(caminho_completo):
            pastas.append((item,caminho_completo))
    return pastas


# Função para listar arquivos de um diretório
def listar_arquivos(diretorio):
    #return [f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))]
    lista_arquivos = []
    for root, dirs, files in os.walk(diretory+"/"+diretorio):
        for file in files:
            path = os.path.join(root, file).replace('\\', '/')
            lista_arquivos.append(path.replace(diretory+"/", ""))
    return lista_arquivos

def criar_grade_imagens(diretorio):
    #pastas = listar_pastas("http://localhost:8000/"+diretorio)
    imagens = listar_arquivos(diretorio)
    
    
    return html.Div([       
            html.Nav(className="navbar", children=[
                html.Div([
                    dcc.Dropdown(
                        id='dropdown-menu',
                        options=[{'label': direc, 'value': item} for direc, item in listar_pastas(diretorio)],
                        value='',
                        className="mx-2",
                        clearable=False,
                        style={'top': '-15px'}
                    )
                ])
            ]),
            html.Br(),
            html.Br(),
            #html.H3(f'Imagens do diretório: {diretorio}', style={'margim-top': '200px'}),
        
        html.Div(id="output-dropdown-value", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})
    ])

@app.callback(
    Output('output-dropdown-value', 'children'),
    [Input('dropdown-menu', 'value'),
     State('dropdown-menu', 'options'),
     State("user-logado", 'data')], 
    prevent_initial_call=True
)
def update_output(value, options, user_logado):
    label = [opt['label'] for opt in options if opt['value'] == value][0]
    return [html.Div([
        html.Div([
            html.Img(src=f'http://{get_ipv4_address()}:8000/{user_logado}/imagens/{label}/{imagem}', style={'width': '100%', 'height': 'auto'}),
            html.P(f'http://{get_ipv4_address()}:8000/{user_logado}/imagens/{label}/{imagem}',  style={'textAlign': 'center'})
        ], style={'textAlign': 'center', 'margin': 'auto', 'width': '50%'})
    ]) for imagem in os.listdir(value)]


