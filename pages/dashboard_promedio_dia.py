import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

dash.register_page(__name__, path='/dashboard_promedio_dia')

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

df['Nivel'] = df[stations].mean(axis=1, skipna=True)
daily_avg_df = df.groupby(['Fecha', 'Parámetro']).agg({
    'Nivel': 'mean'
}).reset_index()

layout = html.Div([
    html.H1("Niveles de contaminación por día"),

    html.Div([
        html.Label('Selecciona una Estación'),
        dcc.Dropdown(
            id='station-dropdown',
            options=[{'label': station.split(' : ')[0], 'value': station} for station in stations],
            value=stations[0],
            multi=False
        )
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.Label('Selecciona un Tipo de Gas'),
        dcc.Dropdown(
            id='gas-dropdown',
            options=[{'label': param, 'value': param} for param in parameters],
            value=parameters[0],
            multi=False
        )
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.Label('Selecciona un Día'),
        dcc.DatePickerSingle(
            id='date-picker',
            min_date_allowed=df['Fecha'].min(),
            max_date_allowed=df['Fecha'].max(),
            date=df['Fecha'].min()
        )
    ], style={'marginBottom': '20px'}),

    html.Div([
        dcc.Graph(id='levels-over-time', style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px'})
    ], style={'marginBottom': '20px'}),

    html.Div([
        dcc.Graph(id='levels-by-station-over-time', style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px'})
    ])
], style={'padding': '20px'})


@dash.callback(
    [Output('levels-over-time', 'figure'),
     Output('levels-by-station-over-time', 'figure')],
    [Input('station-dropdown', 'value'),
     Input('gas-dropdown', 'value'),
     Input('date-picker', 'date')]
)
def update_graphs(selected_station, selected_gas, selected_date):
    filtered_df = df[(df['Fecha'] == selected_date) & (df['Parámetro'] == selected_gas)]

    fig1 = px.line(filtered_df, x='Hora', y=selected_station,
                   title=f'Niveles de {selected_gas} por Hora en {selected_station.split(" : ")[0]} el día {selected_date}',
                   labels={'Hora': 'Hora del Día', selected_station: 'Nivel Promedio'})

    station_avg_df = daily_avg_df[(daily_avg_df['Parámetro'] == selected_gas)]

    fig2 = px.line(station_avg_df, x='Fecha', y='Nivel',
                   title=f'Niveles Promedios Diarios de {selected_gas} en {selected_station.split(" : ")[0]} a lo Largo del Tiempo',
                   labels={'Fecha': 'Fecha', 'Nivel': 'Nivel Promedio'})

    return fig1, fig2
