import dash
from dash import dcc, html, Input, Output
import dash_leaflet as dl

dash.register_page(__name__, path='/')  

# Datos de las estaciones y abreviaturas
stations = {
    'ATI': "Centro de Salud (Atitalaquia)",
    'ATO': "Primaria Revolución (Atotonilco de Tula)",
    'HRE': "Hospital Regional (Tula de Allende)",
    'CSA': "Centro de Salud (Tula de Allende)",
    'UTTT': "Universidad Tecnológica de Tula Tepeji (Tula de Allende)"
}

# Datos de los gases y abreviaturas
gases = {
    'PM10': 'Partículas suspendidas PM10 (µg/m³)',
    'PM2.5': 'Partículas suspendidas PM2.5 (µg/m³)',
    'CO': 'Monóxido de Carbono (ppm)',
    'NO2': 'Dióxido de Nitrógeno (ppm)',
    'O3': 'Ozono (ppm)',
    'SO2': 'Dióxido de Azufre (ppm)'
}

# Marcadores para el mapa
markers = [
    {"position": [20.0072469, -99.2188349], "popup": "Estación Primaria Revolución: Atotonilco de Tula"},
    {"position": [20.0601084, -99.2220583], "popup": "Estación Centro de Salud: Atitalaquia"},
    {"position": [20.0405499, -99.3428569], "popup": "Estación Hospital Regional: Tula de Allende"},
    {"position": [20.0540362, -99.3403668], "popup": "Estación Centro de Salud: Tula de Allende"},
    {"position": [20.0092688, -99.343532], "popup": "Estación Universidad Tecnológica de Tula Tepeji: Tula de Allende"}
]

layout = html.Div([
    html.H1("Bienvenido a la Aplicación de Monitoreo de Calidad del Aire"),
    
    html.P("La Zona Metropolitana de Tula (ZMT), ubicada en el estado de Hidalgo, México, es una región con una creciente actividad industrial y urbana. La interacción entre estas actividades, el tráfico vehicular y otras fuentes de emisiones ha llevado a preocupaciones significativas sobre la calidad del aire. La contaminación atmosférica en esta área puede tener impactos adversos en la salud de los habitantes y en el medio ambiente."),
    
    html.P("Esta aplicación presenta información detallada sobre las estaciones de monitoreo de la calidad del aire en la Zona Metropolitana de Tula, Hidalgo (ZMT), utilizando datos proporcionados por el Sistema Nacional de Información de la Calidad del Aire (SINAICA). Los datos abarcan del 1 de enero de 2016 al 31 de diciembre de 2022."),
    
    html.P("Los seis contaminantes criterio que se incluyen en esta aplicación son:"),

    html.Ul([
        html.Li("Partículas suspendidas (PM10 y PM2.5): Partículas inhalables que pueden causar problemas respiratorios y cardiovasculares."),
        html.Li("Ozono (O3): Un gas que puede irritar las vías respiratorias y empeorar enfermedades respiratorias."),
        html.Li("Dióxido de azufre (SO2): Un gas que puede causar problemas respiratorios y contribuir a la formación de lluvia ácida."),
        html.Li("Dióxido de nitrógeno (NO2): Un gas que puede causar irritación en los pulmones y disminuir la función pulmonar."),
        html.Li("Monóxido de carbono (CO): Un gas incoloro y tóxico que puede interferir con la capacidad del cuerpo para transportar oxígeno."),
    ]),
    
    html.P("Estas estaciones están estratégicamente ubicadas en cinco puntos de la ZMT para recolectar datos y proporcionar análisis sobre la calidad del aire en diferentes áreas."),
    
    html.P("Es importante tener en cuenta que no todas las estaciones miden todos los gases de forma continua. Además, pueden ocurrir días en los que las estaciones no funcionen correctamente o estén fuera de servicio, lo que puede resultar en vacíos de información en los datos presentados. A pesar de estos posibles inconvenientes, la aplicación proporciona una visión general útil sobre la calidad del aire en la ZMT."),

    html.Div([
        html.Div([
            dl.Map([
                dl.TileLayer(),
                *[
                    dl.Marker(
                        position=marker["position"], 
                        children=[dl.Popup(marker["popup"])],
                        id=f"marker-{i}"
                    ) for i, marker in enumerate(markers)
                ]
            ], style={'height': '500px', 'width': '70%', 'borderRadius': '8px', 'boxShadow': '0px 4px 8px rgba(0,0,0,0.2)'}, 
            center=[20.03, -99.28], zoom=12)
        ], style={'width': '70%', 'display': 'inline-block'}),
        
        html.Div([
            html.H3("Estaciones de Monitoreo"),
            html.Ul([
                html.Li(f"{abbr}: {full_name}") for abbr, full_name in stations.items()
            ]),
            dcc.Store(id='selected-marker', data={'popup': ''}),
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px', 'backgroundColor': '#f9f9f9', 'borderRadius': '8px', 'boxShadow': '0px 4px 8px rgba(0,0,0,0.2)'})
    ], style={'marginTop': '20px'}),

    html.Div([
        html.H3("Diccionario de abreviaturas"),
        html.Div([
            html.H4("Estaciones"),
            html.Ul([
                html.Li(f"{abbr}: {full_name}") for abbr, full_name in stations.items()
            ]),
        ], style={'marginBottom': '20px'}),
        html.Div([
            html.H4("Gases"),
            html.Ul([
                html.Li(f"{abbr}: {description}") for abbr, description in gases.items()
            ]),
        ])
    ], style={'marginTop': '20px', 'padding': '20px', 'backgroundColor': '#f9f9f9', 'borderRadius': '8px', 'boxShadow': '0px 4px 8px rgba(0,0,0,0.2)'})
])

@dash.callback(
    Output('selected-marker', 'data'),
    [Input(f"marker-{i}", 'n_clicks') for i in range(len(markers))]
)
def update_popup(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return {'popup': ''}
    
    triggered = ctx.triggered[0]['prop_id'].split('.')[0]
    for marker in markers:
        if f"marker-{markers.index(marker)}" == triggered:
            return {'popup': marker["popup"]}
    
    return {'popup': ''}
