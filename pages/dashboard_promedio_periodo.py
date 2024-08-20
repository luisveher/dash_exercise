import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

dash.register_page(__name__, path='/dashboard_promedio_periodo')

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

layout = html.Div([
    html.H1("Niveles de contaminación promedio por periodo de tiempo"),

    html.Div([
        html.Label('Selecciona un Gas'),
        dcc.Dropdown(
            id='gas-dropdown',
            options=[{'label': param, 'value': param} for param in parameters],
            value=parameters[0],
            multi=False
        )
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.Label('Selecciona una o más Estaciones'),
        dcc.Dropdown(
            id='station-dropdown',
            options=[{'label': station.split(' : ')[0], 'value': station} for station in stations],
            value=stations,
            multi=True
        )
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.Label('Selecciona un Rango de Fechas'),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=df['Fecha'].min().date(),
            end_date=df['Fecha'].max().date(),
            display_format='YYYY-MM-DD'
        )
    ], style={'marginBottom': '20px'}),

    html.Div([
        dcc.Graph(id='average-daily-graph', style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px'})
    ], style={'marginBottom': '20px'}),

    html.Div([
        dcc.Graph(id='all-stations-graph', style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px'})
    ])
], style={'padding': '20px'})


@dash.callback(
    [Output('average-daily-graph', 'figure', allow_duplicate=True),
     Output('all-stations-graph', 'figure', allow_duplicate=True)],
    [Input('gas-dropdown', 'value'),
     Input('station-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')],
     prevent_initial_call=True
)
def update_graphs(selected_gas, selected_stations, start_date, end_date):
    if not selected_gas or not selected_stations or not start_date or not end_date:
        return {}, {}

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_df = df[(df['Parámetro'] == selected_gas) &
                     (df['Fecha'] >= start_date) &
                     (df['Fecha'] <= end_date)]

    filtered_df['Average'] = filtered_df[selected_stations].mean(axis=1, skipna=True)
    daily_avg_df = filtered_df.groupby('Fecha').agg({
        'Average': 'mean'
    }).reset_index()

    avg_daily_fig = px.line(daily_avg_df, x='Fecha', y='Average',
                            title=f'Promedio Diario de {selected_gas} en Estaciones Seleccionadas',
                            labels={'Average': 'Promedio', 'Fecha': 'Fecha'})

    all_stations_avg_df = filtered_df.groupby(['Fecha']).agg({
        station: 'mean' for station in stations
    }).reset_index()

    all_stations_fig = px.line(all_stations_avg_df, x='Fecha', y=stations,
                               title=f'Promedio Diario de {selected_gas} en Todas las Estaciones',
                               labels={'value': 'Promedio', 'Fecha': 'Fecha'},
                               facet_col='variable', facet_col_wrap=3)

    return avg_daily_fig, all_stations_fig
