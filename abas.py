import os
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, State, Output
#import directories 

from app import *

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    #'color': 'white',
    'padding': '6px',
    'line-height': '0.5em'
}

button_style = {
    'margin': '5px',
    'padding': '10px',
    'width': '90px',
    'borderRadius': '5px',
    'backgroundColor': '#4CAF50',
    'color': 'white',
    'border': 'none',
    'cursor': 'pointer'
}

a_style = {
    'margin': '5px',
    'padding': '10px',
    'width': '120px',
    'borderRadius': '5px',
    'backgroundColor': '#8A2BE2',
    'color': 'white',
    'border': 'none',
    'cursor': 'pointer',
    'text-decoration': 'none'
}

layout = html.Div([
    dbc.Row( 
        dcc.Tabs(id='abas', parent_className='custom-tabs')   
    ),
    dbc.Row([
            dbc.Col(
                dbc.Button('Salvar', id='save', color='success', style=button_style)
            ),
            dbc.Col(
                html.A('Abrir Página HTML', id='open-html-link', href='/render', target='_blank', style=a_style)
            ),
            # dbc.Col(
            #     dbc.Button('Diretorios', id='crie-diretorios-arq', style=button_style)
            # ),
            dbc.Col(
                html.A('Abrir Imagens', id='open-html-link-imagen', href='/imagens', target='_blank', style=a_style)
            ),
            dbc.Col(
                html.A('Materiais de Apoio', id='open-pdf', href='/pdf', target='_blank', style=a_style)
            ),
            dbc.Col([
                dcc.Interval(
                    id='interval-open-msg', 
                    interval=3000,  # Intervalo de 2 segundos
                    n_intervals=0
                ),
                html.Div(id='msg-salvo',style={'display': 'none'}),
            ])
        ], style={'display': 'flex',
                  'flex-direction': 'row',
                  'justify-content': 'left',
                  'padding-left': '10px',
                  'align-items': 'center'}
    ), 
    dbc.Row(html.Div(id='teste')),
])

@app.callback(
    Output('msg-salvo', 'style'),
    [Input('save', 'n_clicks'),
     Input('interval-open-msg', 'n_intervals'),
     #Input('interval-close-msg', 'n_intervals')
     ],
    prevent_initial_call=True
)
def display_message(btn_save, n_intervals):
    ctx = dash.callback_context
    if ctx.triggered_id == 'save':
        return {'display': 'block',  'background-color':'rgba(255, 215, 0, 0.5)', 'padding': '5px'}  # Exibe a mensagem quando o botão é clicado

    if n_intervals > 1:
        return {'display': 'none'}  # Oculta a mensagem após 2 segundos

# Callback para abrir o modal
# @app.callback(
#     Output("modal-directory", "is_open"),
#     [Input("crie-diretorios-arq", "n_clicks"), Input("close-modal", "n_clicks")],
#     [State("modal-directory", "is_open")],
# )
# def toggle_modal(open_clicks, close_clicks, is_open):
#     if open_clicks or close_clicks:
#         return not is_open
#     return is_open          

@app.callback(
    Output('open-html-link', 'href'),
    Input('abas', 'value'),
    prevent_initial_call=True
)
def aba_selected(selected):
    if selected is None:
        raise PreventUpdate
    return f'/render/{selected}'
                  



"""
[
        dcc.Tab(label="Editor 1", children=[
                dbc.Card([ 
                    dcc.Textarea('informe o valor', style={'width': '100%', 'height': '45vw'})
                ], body=True)
            ], style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label="Editor 1", children=[
                dbc.Card([ 
                    dcc.Textarea('informe o valor', style={'width': '100%', 'height': '45vw'})
                ], body=True)
            ], style=tab_style, selected_style=tab_selected_style)
    ], style={'height':'25px'}
"""
