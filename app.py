#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 22:37:49 2024

@author: andre
"""

import dash
import dash_bootstrap_components as dbc

estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", dbc.themes.DARKLY]
dbc_css = "https://kit.fontawesome.com/a076d05399.js" 

app = dash.Dash(__name__, external_stylesheets=estilos)

app.config['suppress_callback_exceptions'] = True
app.scripts.config.serve_locally = True
server = app.server