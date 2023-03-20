from dash import Dash,html,page_container
import dash_bootstrap_components as dbc

app = Dash(__name__,use_pages=True,external_stylesheets=[dbc.themes.SPACELAB])
app.layout = dbc.Container([
    dbc.NavbarSimple([
        dbc.NavItem(dbc.NavLink("Material",href="nk"))
    ],
    brand='Optical Simulation',brand_href='/',dark=True,color='primary'),

    page_container
])
if __name__ == '__main__':
    app.run_server(debug=True)