import os
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from app import  *

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Função para listar os diretórios
def listar_arquivos(diretorio):
    #return [f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))]
    lista_arquivos = []
    for root, dirs, files in os.walk(diretory+"/"+diretorio):
        for file in files:
            path = os.path.join(root, file).replace('\\', '/')
            lista_arquivos.append(path.replace(diretory+"/", ""))
    return lista_arquivos

# Layout do modal
modal = html.Div(dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Escolha a pasta")),
                dbc.ModalBody(id="modal-body"),
                dbc.ModalFooter(
                    [
                        dbc.Button("Fechar", id="close-modal", className="ml-auto"),
                    ]
                ),
            ],
            id="modal-directory",
            is_open=False,
            className="modal-lg",  # Define o tamanho do modal
            style={"position": "absolute", "left": "50%", "top": "50%", "transform": "translate(-50%, -50%)",
                   "z-index": 10000, "background-color": "white"}
        ))



# Callback para atualizar o conteúdo do modal com a árvore de diretórios
@app.callback(
    Output("modal-body", "children"),
    [Input("modal-directory", "is_open")]
)
def update_modal_body(is_open):
    if is_open:
        caminho_atual = '/conteudos/1c/andre'
        diretorios = listar_arquivos(caminho_atual)
        links = [
            dbc.NavLink(diretorio, href=f"/{diretorio}", className="nav-link")
            for diretorio in diretorios
        ]
        return dbc.Nav(links, vertical=True)
    else:
        return "teste"

# Callback para criar pasta ou arquivo
# @app.callback(
#     Output('output-criacao', 'children'),
#     [Input('criar-btn', 'n_clicks')],
#     [State('tipo', 'value'),
#      State('nome', 'value'),
#      State("modal", "is_open")]
# )
# def criar(n_clicks, tipo, nome, is_modal_open):
#     if n_clicks > 0:
#         if nome:
#             caminho_completo = os.path.join(os.getcwd(), nome)
#             if tipo == 'pasta':
#                 if not os.path.exists(caminho_completo):
#                     os.makedirs(caminho_completo)
#                     return f"Pasta '{nome}' criada com sucesso!"
#                 else:
#                     return f"A pasta '{nome}' já existe."
#             elif tipo == 'arquivo':
#                 if not os.path.exists(caminho_completo):
#                     with open(caminho_completo, 'w') as f:
#                         f.write("")
#                     return f"Arquivo '{nome}' criado com sucesso!"
#                 else:
#                     return f"O arquivo '{nome}' já existe."
#         else:
#             return "Por favor, insira um nome."
#     else:
#         return ""

