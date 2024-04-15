import os
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, State, Output, ALL
from dash_bootstrap_components import Modal, ModalHeader, ModalBody, ModalFooter
from app import *

import json
import base64
#import asyncio
#import aiohttp
import list_files

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

def criar_grade_pdf(diretorio):
    return dbc.Row([
            html.Div(#id='directorys',
                list_files.gererate_list_files_pdf(diretorio),
                style={'width': '120px',  'height': '89vh',
                        'float': 'left',
                        'margin': '0', 'border': '2px solid #000',
                        'padding': '5px -10px 5px 5px'}
            ),
            html.Div(id='output-pdfs')
        ])

@app.callback(
    Output('output-pdfs', 'children'),
    [Input({'type': 'item-pdf', 'index': ALL}, 'n_clicks')],
    prevent_initial_call=True
)
def open_pdf(n_clicks):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        raise PreventUpdate

    clicked_id = json.loads(ctx.triggered[0]['prop_id'].rsplit('.', 1)[0])
        
    try:
        with open(clicked_id['index'], "rb") as file:
           pdf_content = base64.b64encode(file.read()).decode('utf-8')
           return html.Iframe(src=f"data:application/pdf;base64,{pdf_content}", style={'width': '85vw', 'height': '96vh', 'border': 'none'})
    except Exception as e:
        return html.Div(f"Erro ao abrir o PDF: {str(e)}", style={'color': 'red'})
    

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


