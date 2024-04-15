import os
from dash import html, dcc
import dash_bootstrap_components as dbc
from app import *

directory = os.path.abspath(diretory)

def generate_items(name, path, level):
    if os.path.isdir(path):
        return html.Details([
                    html.Summary(name, style={"cursor": 'pointer'}),
                    dbc.NavLink(
                        gererate_list_files(path, level+1),
                        style={'list-style-type': 'none'},
                    )
              ], style={'padding-left': '10px'})   
    else:
        return dbc.NavLink(html.Div(name, className="nav-link-custom", style={'padding-left': '10px'}), id={'type': 'item', 'index': path}, 
                       style={'cursor': 'pointer','list-style-type': 'none',
                              'margin-bottom': '2px'})

def gererate_list_files(directory, level=0):
    directory_content = os.listdir(directory)
    directory_content.sort(key=lambda x: os.path.isfile(os.path.join(directory, x)))
    
    items = []
    for item in directory_content:
        full_path = os.path.join(directory, item)
        items.append(generate_items(item, full_path, level))
    return items 

def generate_items_pdf(name, path, level):
    if os.path.isdir(path):
        return html.Details([
                    html.Summary(name, style={"cursor": 'pointer'}),
                    dbc.NavLink(
                        gererate_list_files_pdf(path, level+1),
                        style={'list-style-type': 'none'},
                    )
              ], style={'padding-left': '10px'})   
    else:
        return dbc.NavLink(html.Div(name, className="nav-link-custom", style={'padding-left': '10px'}), id={'type': 'item-pdf', 'index': path}, 
                       style={'cursor': 'pointer','list-style-type': 'none',
                              'margin-bottom': '2px'})

def gererate_list_files_pdf(directory, level=0):
    directory_content = os.listdir(directory)
    directory_content.sort(key=lambda x: os.path.isfile(os.path.join(directory, x)))
    
    items = []
    for item in directory_content:
        full_path = os.path.join(directory, item)
        items.append(generate_items_pdf(item, full_path, level))
    return items 