from dash import html, dcc
from dash.dependencies import Input, State, Output, ALL
import dash_bootstrap_components as dbc
from dash_ace import DashAceEditor
from dash.exceptions import PreventUpdate
import os
import json
import re

import flask
from app import *
import list_files
import abas


app.layout = dbc.Container([
    dcc.Store(id="tabs-html"),
    dcc.Location('url', refresh=True),
    html.Div(id='content'),
], style={"margin": '5px'})

def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return html_content

@app.callback(
    Output('content', 'children'),
    Input('url', 'pathname'),
)
def display(pathname):
    if pathname == '/':
        layout = [
            list_files.layout,
            abas.layout
        ]
        return layout
    elif pathname == '/render':
        arq = os.path.abspath('conteudos/index.html')
        return html.Iframe(sandbox='', srcDoc=read_html_file(arq), style={'background-color': 'white', 'width': '100vw', 'height': '100vh', 'margin-left': '-10px'})




@app.callback(
    Output('tabs-html', 'data'),
    Output('abas', 'children'),
    [Input({'type': 'item', 'index': ALL}, 'n_clicks')],
    [State('abas', 'children'),
     State('tabs-html', 'data')],
    prevent_initial_call=True
)
def abas_(n_clicks, tabs, tabs_html_criated):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        raise PreventUpdate
    
    if 1 in n_clicks:#ctx.triggered:
        clicked_id = json.loads(ctx.triggered[0]['prop_id'].rsplit('.', 1)[0])
        
        if tabs is None:
            tabs = []
            
        if tabs_html_criated is None:
            tabs_html_criated = []
                     
        if os.path.basename(clicked_id['index']) not in  tabs_html_criated:
           name_file = os.path.basename(clicked_id['index']).split('.')[0]
           
           html_content = read_html_file(clicked_id['index'])
            
           new_tabs = dcc.Tab(label=name_file, children=[ 
                    dbc.Card([ 
                        DashAceEditor(id={'type': 'textarea', 'index': clicked_id['index']},
                                     value=read_html_file(clicked_id['index']), 
                                     theme="github",
                                     mode='html',
                                     tabSize=2,
                                     enableBasicAutocompletion=True,
                                     enableLiveAutocompletion=True,
                                     autocompleter="/autocompleter?prefix=")
                    ], body=True)
            ])
           tabs.append(new_tabs)
           tabs_html_criated.append(os.path.basename(clicked_id['index']))
            
           return tabs_html_criated, tabs
        else:
            raise PreventUpdate 
    raise PreventUpdate

@app.callback(
    Output('teste', 'children'),
    Input('save', 'n_clicks'),
    [State({'type': 'textarea', 'index': ALL}, 'id'),
    State({'type': 'textarea', 'index': ALL}, 'value')],
    prevent_initial_call=True
)
def save_textarea(btn_save, textareas_id, textarea_value):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    ctx = dash.callback_context
    
    if btn_save or changed_id == 'save.n_clicks':
        #clicked_id = json.loads(ctx.triggered[0]['prop_id'])#.rsplit('.', 1)[0])
        cont = 0
        for index, id in enumerate(textareas_id):
            with open(id['index'], 'w') as file:
                file.write(textarea_value[index])
        return textarea_value#'arquivo salvo!'
                         
     
    raise PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True, host='192.168.15.11')


