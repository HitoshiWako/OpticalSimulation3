import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from dash import html,dcc,callback,Input,Output,State,dash_table

import opticalsimulation.database as db
import opticalsimulation.opticalsimulation as op

dash.register_page(__name__,path='/')



layout = dbc.Container([
    html.H2('Spectra'),
    dbc.Row(
    [
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(dcc.Graph(id='graph-reflect'),label='Reflectance'),
                dbc.Tab(dcc.Graph(id='graph-trans'),label='Transmittance'),
                dbc.Tab(dcc.Graph(id='graph-reflect-with-back'),label='Reflectance(with back reflection)')
            ])
        ]),
        dbc.Col([
            html.Div([
                dbc.Label(id='label-angle'),
                dcc.Slider(id='slider-angle',min=0,max=89.9,step=0.1,value=0,marks={0:'0',5:'5',12:'12',45:'45'}),
            ]),
            html.Br(),
            html.Div([
                dbc.Label('Layers'),
                dash_table.DataTable(id='table_layer',
                                     data=[],
                                     columns=[{'id':'name','name':'Material','presentation':'dropdown'},
                                              {'id':'thickness','name':'Thickness','type':'numeric'}],
                                     style_header={'textAlign':'left'},
                                     style_cell={'height':0},
                                     style_cell_conditional=[{
                                        'if':{'column_id':'name'},'textAlign':'left'
                                     }],
                                     editable=True,
                                     row_deletable=True,
                                     dropdown={
                                        'name':{
                                            'options':[{'label':mat[1],'value':mat[0]} for mat in db.get_material_list()]
                                        }
                                     }
                ),
                html.Div([dbc.Button('Add Layer',id='button_add_layer',n_clicks=0,style={'margin-top':10})],
                         className="d-md-flex justify-content-md-end"),
            ]),
            html.Br(),
            html.Div([
                dbc.Label('Substrate'),
                dcc.Dropdown(id='substrate',options=[{'label':mat[1],'value':mat[0]} for mat in db.get_material_list()]),
                dbc.InputGroup([
                    dbc.InputGroupText('Thcikness'),
                    dbc.Input(id='substrate-thickness',type='number',min=0),
                    dbc.InputGroupText('um')
                ], style={'padding-top':10}),
            ])
        ],width=3)
    ]
    )
])

@callback(
    Output('label-angle','children'),
    Output('graph-reflect','figure'),
    Output('graph-trans','figure'),    
    Output('graph-reflect-with-back','figure'),
    Input('slider-angle','value'),
    Input('substrate','value'),
    Input('substrate-thickness','value')
)
def update_angle(angle,substrate,thickness):
    fig_ref1 = go.Figure()
    fig_ref2 = go.Figure()
    fig_trans = go.Figure()

    if substrate is not None:
        nks = db.get_opticalindex(substrate)
        min_wl = min(nks[0])
        max_wl = max(nks[0])
        step=10
        wl = np.arange(min_wl,max_wl,step)
        n0 = 1
        n2 = 1
        n1 = np.array(db.fitted_opticalindex(substrate,min_wl,max_wl,step))
        if thickness is not None:            
            ref1,_,ref2,trans = op.calc_spectra(n0,n1,n2,angle,[],[],[],[],thickness,wl)
            fig_ref1.add_trace(go.Scatter(x=wl,y=ref1[0], mode='lines'))
            fig_ref1.add_trace(go.Scatter(x=wl,y=ref1[1], mode='lines'))
            fig_trans.add_trace(go.Scatter(x=wl,y=trans[0], mode='lines'))
            fig_trans.add_trace(go.Scatter(x=wl,y=trans[1], mode='lines'))
            fig_ref2.add_trace(go.Scatter(x=wl,y=ref2[0], mode='lines'))
            fig_ref2.add_trace(go.Scatter(x=wl,y=ref2[1], mode='lines'))
        else:
            thickness=1
            ref1,trans,_,_ = op.calc_spectra(n0,n1,n2,angle,[],[],[],[],thickness,wl)
            fig_ref1.add_trace(go.Scatter(x=wl,y=ref1[0], mode='lines'))
            fig_ref1.add_trace(go.Scatter(x=wl,y=ref1[1], mode='lines'))
            fig_trans.add_trace(go.Scatter(x=wl,y=trans[0], mode='lines'))
            fig_trans.add_trace(go.Scatter(x=wl,y=trans[1], mode='lines'))
            fig_ref2.add_trace(go.Scatter(x=wl,y=ref1[0], mode='lines'))
            fig_ref2.add_trace(go.Scatter(x=wl,y=ref1[1], mode='lines'))
    return 'Incident Angle: {:.1f}'.format(angle),fig_ref1,fig_trans,fig_ref2

@callback(
    Output('table_layer','data'),
    Input('button_add_layer','n_clicks'),
    State('table_layer','data'),
    State('table_layer','columns')
)
def add_layer(n_clicks, data, columns):
    if n_clicks > 0:
        data.append({c['id']:'' for c in columns})
    return data
