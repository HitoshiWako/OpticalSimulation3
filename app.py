from dash import Dash, html,dcc, dash_table,Input,Output,State
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import opticalsimulation.database as db


table_data = [{'id':d[0],'name':d[1]} for d in db.get_material_list()]

app = Dash(external_stylesheets=[dbc.themes.SPACELAB])

app.layout = dbc.Container([
    html.H1("Optical Index"),
    html.Hr(),
    dbc.Col(dcc.Graph(id='nk_graph')),
    dash_table.DataTable(id='material_list_table',
                         data=table_data,
                         columns=[{"id":"name","name":"Material"}],
                         style_cell={'textAlign':'left'},
                         row_selectable='single')
])

@app.callback(
    Output('nk_graph','figure'),
    Output('material_list_table','selected_rows'),
    Input('material_list_table','selected_rows'),
    State('material_list_table','data')
)
def show_selected_nk(selected_rows,tbl):
    if not selected_rows:
        selected_rows = [0]
    id = tbl[selected_rows[0]]['id']
    nks = db.get_opticalindex(id)
    ns = [nk.real for nk in nks[1]]
    ks = [-nk.imag for nk in nks[1]]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=nks[0],y=ns,mode='lines',name='n'))
    fig.add_trace(go.Scatter(x=nks[0],y=ks,mode='lines',name='k'))
    return fig,selected_rows

if __name__ == '__main__':
    app.run_server(debug=True)
