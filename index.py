from dash import html, dcc
from dash.dependencies import Input, State, Output, ALL
import dash_bootstrap_components as dbc
from dash_ace import DashAceEditor
from dash.exceptions import PreventUpdate
#from dash_html_components import Iframe
#import dash_dangerously_set_inner_html

import os
import json 
#import re 
#import base64

#import flask
from flask_login import current_user

from app import *
import list_files
import abas
import login
import register
import list_itens_to_tab
#import directories


login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

app.layout = dbc.Container(id='container', children=[
    dcc.Store(id="tabs-html"),
    dcc.Store(id="user-logado"),
    dcc.Store(id='store-login-status'),
    dcc.Location('url'),
    dcc.Store(id='rotas-url', data='/'),
    dcc.Store(id='register-state'),
    html.Div(id='content')
], style={"margin": '5px'})

def read_html_file(file_path):
    encodings = ['utf-8', 'latin1']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                html_content = file.read()
            return html_content
        except UnicodeDecodeError:
            pass
def login1():
    return "alert('Você clicou no botão de login!');"
    
@app.callback(
    Output('url', 'pathname'),
    Input('rotas-url', 'data'),
    prevent_initial_call=True
)
def iniciar(rotas):
   if rotas == None or rotas == "":
        raise PreventUpdate
    
   ctx = dash.callback_context
   if ctx.triggered:
        trigg_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if trigg_id == 'rotas' or rotas == '/ide':
            return '/ide'   
        if rotas == '/register':
            return '/register'   
   return '/'

@login_manager.user_loader
def load_user(user_id):
    return session.query(Users).get(int(user_id))

@app.callback(
    Output('content', 'children'),
    Output('user-logado', 'data'),
    Input('url', 'pathname'),
    #State('directory', 'data'),
    #[State('tab-selected', 'data')]
)
def display(pathname):
    
    if pathname == '/' or pathname == '/login':
        layout = [
            login.layout
        ]
        return layout, ""
    if pathname == '/ide':
        user = ""
        if current_user.is_authenticated:
            user = current_user.username
            layout = [
                #list_files.layout,
                dbc.Row([
                    html.Label(f'Nome do usuário: {current_user.username}')
                ], style={"margin-bottom": '5px'}),
                dbc.Row([
                    html.Div(#id='directorys',
                        list_files.gererate_list_files(diretory+'\\'+user),
                        style={'width': '120px',  'height': '89vh',
                                'float': 'left',
                                'margin': '0', 'border': '2px solid #000',
                                'padding': '5px -10px 5px 5px'}
                    ),
                    abas.layout
                ]),
                
                #directories.modal
            ]
        else:
            layout = [login.layout]
        return layout, user
    if pathname == '/register':
        if current_user.is_authenticated and current_user.username == 'admin':
            return register.render_layout(""), ""
        else:
            return [login.layout], ""
    
    if pathname.startswith('/render/'):
        if current_user.is_authenticated:
            user = current_user.username
            #file = f"{pathname.split('/')[-1]}.html"
            file = pathname.split('/render/')[1].strip()
            path = file
            #path = f"{diretory}/{user}/{file}.html"
            #for root, dirs, files in os.walk(diretory+"/"+user):
            #     if file in files:
            #         path = os.path.abspath(os.path.join(root, file))
            print(path)
            if os.path.exists(path):
                arq = os.path.abspath(path)
                #return dash_dangerously_set_inner_html.DangerouslySetInnerHTML(children=read_html_file(arq))
                return html.Div(html.Iframe(srcDoc=read_html_file(arq), style={"height": "99vh", "width": "99vw", 'margin': '-10px'})), user
            
            return [login.layout], ""
            
    if pathname == '/imagens':
        if current_user.is_authenticated:
            user = current_user.username
            return html.Div([
                list_itens_to_tab.criar_grade_imagens(diretory+'/'+user+'/imagens')
            ]), user
        else:
            return [login.layout], ""
    
    if pathname == '/pdf':
        if current_user.is_authenticated:
            user = current_user.username
            return html.Div([
                list_itens_to_tab.criar_grade_pdf('conteudos/apoio')
            ]), user
        
    return html.Div([
            dbc.Card([
                html.B("Erro 404 Not Found", style={'font-size': '2em'}) 
            ])
         ], style={'display': 'flex', 'justify-content': 'center'}), ""
      
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
    print(ctx.triggered[0]['prop_id'])
    
    if 1 in n_clicks:#ctx.triggered:
        clicked_id = json.loads(ctx.triggered[0]['prop_id'].rsplit('.', 1)[0])
        
        if tabs is None:
            tabs = []
            
        if tabs_html_criated is None:
            tabs_html_criated = []
        
                     
        #if os.path.basename(clicked_id['index']) not in  tabs_html_criated:
        if clicked_id['index'] not in  tabs_html_criated:
           name_file = os.path.basename(clicked_id['index']).split('.')[0]
           file_format = os.path.basename(clicked_id['index']).split('.')[-1]
           
           html_content = read_html_file(clicked_id['index'])
           
           if file_format in ('html', 'css', 'js'):
               new_tabs = dcc.Tab(
                    label=name_file,
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    value=clicked_id['index'],#name_file,
                    children=[ 
                        # dbc.Row(
                        #     html.Button("X", 
                        #                 id={'type': 'close-button-tab', 'index': clicked_id['index']},
                        #                 style={'margin-top': '-20px', 
                        #                        'borderRadius': '5px',
                        #                        'backgroundColor': '#4CAF50',
                        #                        'color': 'white',
                        #                        'border': 'none',
                        #                        'fontSize': '20px',
                        #                        'cursor': 'pointer'}),
                        #     style={'display': 'flex', 'justify-content': 'left'}
                        # ),
                        dbc.Row([ 
                            DashAceEditor(id={'type': 'textarea', 'index': clicked_id['index']},
                                         value=read_html_file(clicked_id['index']), 
                                         theme="monokai",
                                         mode='html',
                                         tabSize=2,
                                         height='75vh',
                                         width='60wh',
                                         enableBasicAutocompletion=True,
                                         enableLiveAutocompletion=True,
                                         autocompleter="/autocompleter?prefix=")
                        ])
                ])
               tabs.append(new_tabs)
               tabs_html_criated.append(clicked_id['index'])#os.path.basename(clicked_id['index']))
                
               return tabs_html_criated, tabs
           else:
               raise PreventUpdate 
        else:
            raise PreventUpdate 
    raise PreventUpdate

@app.callback(
    Output('msg-salvo', 'children'),
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
        return 'Arquivo salvo!'
     
    raise PreventUpdate


if __name__ == '__main__': 
    app.run_server(debug=True, host=get_ipv4_address())


