from dash import Dash, html,dcc
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import opticalsimulation.database as db

nks = db.get_opticalindex(1)
ns = [nk.real for nk in nks[1]]
ks = [-nk.imag for nk in nks[1]]
fig = go.Figure()
fig.add_trace(go.Scatter(x=nks[0],y=ns,mode='lines'))
fig.add_trace(go.Scatter(x=nks[0],y=ks,mode='lines'))

app = Dash(external_stylesheets=[dbc.themes.SPACELAB])

app.layout = dbc.Container([
    html.H1("Optical Index"),
    html.Hr(),
    dbc.Col(dcc.Graph(figure=fig)),
])

if __name__ == '__main__':
    app.run_server(debug=True)
