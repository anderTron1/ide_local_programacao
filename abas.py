import os
from dash import html, dcc
import dash_bootstrap_components as dbc

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px',
    'line-height': '0.5em'
}

layout = html.Div([
    dbc.Row( 
        dcc.Tabs(id='abas')   
    ),
    dbc.Row([
            dbc.Col(
                dbc.Button('Salvar', id='save', color='success', style={'width': '90px'})
            ),
            dbc.Col(
                html.A('Abrir Página HTML', id='open-html-link', href='/render', target='_blank')
            )
        ], style={'display': 'flex', 'flex-direction': 'row', 
                  'justify-content': 'left', 'padding-left': '10px',
                  'padding-top': '10px'}
    ),
    dbc.Row(html.Div(id='teste'))
])
                  

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
