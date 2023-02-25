from dash import Dash, html,dcc
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

x = np.arange(10)
fig = go.Figure(
    data=go.Scatter(x=x,y=x**2,mode='lines')
)

app = Dash(external_stylesheets=[dbc.themes.SPACELAB])

app.layout = dbc.Container([
    html.H1("Optical Index"),
    html.Hr(),
    dbc.Col(dcc.Graph(figure=fig)),
])

if __name__ == '__main__':
    app.run_server(debug=True)
