from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc

app = Dash(__name__,use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])

app.layout = dbc.Container([
	html.H1('Optical Simulation'),

	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True)