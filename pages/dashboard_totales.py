import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

dash.register_page(__name__, path='/dashboard_totales')

file_path = "C:/Users/JoseL/Downloads/Datos estaciones/Proyecto_final/archivo_combinado.csv"
df = pd.read_csv(file_path)

df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Hora'] = pd.to_numeric(df['Hora'], errors='coerce')

stations = ['ATI : Centro de Salud', 'ATO : Primaria Revolución',
            'HRE : Hospital Regional', 'CSA : Centro de Salud',
            'UTTT : Universidad Tecnológica de Tula Tepeji']

for station in stations:
    df[station] = pd.to_numeric(df[station], errors='coerce')

parameters = df['Parámetro'].unique()

units = {
    'PM10': 'µg/m³ (microgramos/metro cúbico)',
    'PM2.5': 'µg/m³ (microgramos/metro cúbico)',
    'CO': 'ppm (partes por millón)',
    'NO2': 'ppm (partes por millón)',
    'O3': 'ppm (partes por millón)',
    'SO2': 'ppm (partes por millón)'
}

layout = html.Div([
    html.H1("Niveles de contaminación total por periodo"),

    html.Label('Selecciona una o más Estaciones'),
    dcc.Dropdown(
        id='station-dropdown',
        options=[{'label': station.split(' : ')[0], 'value': station} for station in stations],
        value=stations,
        multi=True
    ),

    html.Label('Selecciona un Rango de Fechas'),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=df['Fecha'].min().date(),
        end_date=df['Fecha'].max().date(),
        display_format='YYYY-MM-DD'
    ),

    html.Div(id='emissions-sum-graphs', style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '20px', 'marginTop': '20px'}),

    html.Div([
        dcc.Graph(id='other-gases-pie-graph', style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px'}),
    ], style={'marginTop': '20px'}),

    html.Div(id='pm-emissions-sum-graphs', style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '20px', 'marginTop': '20px'}),

    html.Div([
        dcc.Graph(id='pm-pie-graph', style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px'}),
    ], style={'marginTop': '20px'}),

])

@dash.callback(
    [Output('emissions-sum-graphs', 'children'),
     Output('pm-pie-graph', 'figure'),
     Output('other-gases-pie-graph', 'figure'),
     Output('pm-emissions-sum-graphs', 'children')],
    [Input('station-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')],
    prevent_initial_call=True
)
def update_emissions_summary(selected_stations, start_date, end_date):
    if not selected_stations or not start_date or not end_date:
        return [], {}, {}, []

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_df = df[(df['Fecha'] >= start_date) & (df['Fecha'] <= end_date)]

    gas_summaries = []
    pm_summaries = []
    pm_data = {'Parámetro': [], 'Emisiones': []}
    other_gases_data = {'Parámetro': [], 'Emisiones': []}

    for param in parameters:
        param_df = filtered_df[filtered_df['Parámetro'] == param]

        if param_df.empty:
            continue

        total_emissions = param_df[selected_stations].sum().sum()

        unit = units.get(param, 'N/A')

        summary_card = html.Div([
            html.H3(param),
            html.P(f'Emisiones Totales: {total_emissions:.2f} {unit}', style={'fontSize': '24px', 'fontWeight': 'bold'}),
        ], style={'border': '1px solid #ddd', 'borderRadius': '8px', 'padding': '20px', 'boxShadow': '0px 4px 8px rgba(0,0,0,0.2)', 'textAlign': 'center', 'flex': '1', 'backgroundColor': 'white'})

        if param in ['PM10', 'PM2.5']:
            pm_summaries.append(summary_card)
            pm_data['Parámetro'].append(param)
            pm_data['Emisiones'].append(total_emissions)
        else:
            gas_summaries.append(summary_card)
            other_gases_data['Parámetro'].append(param)
            other_gases_data['Emisiones'].append(total_emissions)

    if len(pm_data['Parámetro']) > 0:
        pm_pie_fig = px.pie(pm_data, names='Parámetro', values='Emisiones', title='Distribución de Emisiones: PM10 y PM2.5')
    else:
        pm_pie_fig = {}

    if len(other_gases_data['Parámetro']) > 0:
        other_gases_pie_fig = px.pie(other_gases_data, names='Parámetro', values='Emisiones', title='Distribución de Emisiones: SO2, CO, NO2 y O3')
    else:
        other_gases_pie_fig = {}

    return gas_summaries, pm_pie_fig, other_gases_pie_fig, pm_summaries
