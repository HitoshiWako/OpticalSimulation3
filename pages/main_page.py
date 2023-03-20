import dash
import dash_bootstrap_components as dbc
from dash import html,dcc,callback,Input,Output,State,dash_table

import opticalsimulation.database as db

#substrate_list =[item[1]  for item in db.get_material_list()]

dash.register_page(__name__,path='/')



layout = dbc.Container([
    html.H2('Spectra'),
    dbc.Row(
    [
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(dcc.Graph(id='graph_reflect'),label='Reflectance'),
                dbc.Tab(dcc.Graph(id='graph_trans'),label='Transmittance'),
                dbc.Tab(dcc.Graph(id='graph_reflect_with_back'),label='Reflectance(with back reflection)')
            ])
        ]),
        dbc.Col([
            html.Div([
                dbc.Label(id='label_angle'),
                dcc.Slider(id='slider_angle',min=0,max=89.9,step=0.1,value=0,marks={0:'0',5:'5',12:'12',45:'45'}),
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
                    dbc.Input(type='number',min=0),
                    dbc.InputGroupText('mm')
                ],style={'padding-top':10}),
            ])
        ],width=3)
    ]
    )
])

@callback(
    Output('label_angle','children'),
    Input('slider_angle','value')
)
def update_angle(angle):
    return 'Incident Angle: {:.1f}'.format(angle)

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
