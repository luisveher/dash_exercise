import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import page_container

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    
    html.Header([
        html.Div([
            html.Div("Monitoreo de calidad del aire", className="logo"),
            html.Nav([
                html.Ul([
                    html.Li(dcc.Link('Inicio', href='/', className='nav-link')),
                    html.Li(dcc.Link('Mediciones totales', href='/dashboard_totales', className='nav-link')),
                    html.Li(dcc.Link('Mediciones por periodo de tiempo', href='/dashboard_promedio_periodo', className='nav-link')),
                    html.Li(dcc.Link('Mediciones por día', href='/dashboard_promedio_dia', className='nav-link')),
                ], className="nav-links"),
            ]),
        ], className="header-content")
    ], className="header"),
    
    html.Main([
        page_container
    ]),
    
    html.Footer([
        html.P("© 2024 Monitoreo de Calidad del Aire. Todos los derechos reservados.")
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
