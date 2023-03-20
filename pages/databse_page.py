import requests
import dash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import opticalsimulation.database as db
from dash import html,dcc,dash_table,Input,Output,State,ctx,callback

dash.register_page(__name__,path='/nk')

layout = dbc.Container([
    html.H2("Optical Index Database"),
    html.Hr(),
    dbc.Alert('Illigal URL',id='url_alert',is_open=False,duration=2000),
    dbc.Col(dcc.Graph(id='nk_graph')),
    dbc.Row([
        dbc.Col([dbc.Input(id='input_url',placeholder='Input URL',type='url')]),
        dbc.Col([dbc.Button('Load',id='input_button',color='primary',n_clicks=0)]),
    ]),
    html.Br(),
    dash_table.DataTable(id='material_list_table',
                         data = [],
                         columns=[{"id":"name","name":"Material"}],
                         style_cell={'textAlign':'left'},
                         row_selectable='single'),
    html.Br()
])

@callback(
    Output('material_list_table','data'),
    Output('input_url','value'),
    Output('url_alert','is_open'),
    Input('input_button','n_clicks'),
    State('input_url','value')
)
def load_new_material(n_clicks,url):
    is_open = False
    if 'input_button' == ctx.triggered_id:
        if url.rsplit('/',1)[0] == 'https://www.filmetricsinc.jp/technology/refractive-index-database/download':
            try:
                db.add_opticalindex(url)
            except requests.exceptions.RequestException as e:
                is_open = True
        else:
            is_open = True
    return [{'id':d[0],'name':d[1]} for d in db.get_material_list()],'',is_open

@callback(
    Output('nk_graph','figure'),
    Output('material_list_table','selected_rows'),
    Input('material_list_table','selected_rows'),
    State('material_list_table','data')
)
def show_selected_nk(selected_rows,tbl):
    if tbl:
        id = tbl[selected_rows[0]]['id']
        nks = db.get_opticalindex(id)
        ns = [nk.real for nk in nks[1]]
        ks = [-nk.imag for nk in nks[1]]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=nks[0],y=ns,mode='lines',name='n'))
        fig.add_trace(go.Scatter(x=nks[0],y=ks,mode='lines',name='k'))
        return fig,selected_rows
    else:
        return go.Figure(),[]
