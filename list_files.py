import os
from dash import html, dcc

directory = '/home/andre/Documentos/Documentos/MINHAS AULAS/FUNAPE/sistema/conteudos'

def generate_items(name, path, level):
    if os.path.isdir(path):
        return html.Details([
                    html.Summary(name, style={"cursor": 'pointer'}),
                    html.Ul(
                        gererate_list_files(path, level+1),
                        style={'list-style-type': 'none', 'padding-left': '10px'}
                        
                    ) 
              ])  
    else:
        return html.Li(name, id={'type': 'item', 'index': path}, 
                       style={'cursor': 'pointer','list-style-type': 'none',
                              'margin-bottom': '2px', 'color': 'white'})

def gererate_list_files(directory, level=0):
    directory_content = os.listdir(directory)
    directory_content.sort(key=lambda x: os.path.isfile(os.path.join(directory, x)))
    
    items = []
    for item in directory_content:
        full_path = os.path.join(directory, item)
        items.append(generate_items(item, full_path, level))
    return items 

layout = html.Div(
    gererate_list_files(directory),
    style={'width': '200px',  'height': '99vh',
           'float': 'left',
           'margin': '0', 'border': '2px solid #000',
           'padding': '5px'}
)
