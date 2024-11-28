import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from datetime import datetime, timedelta

# import project packages
import helpers.datas as datas # store links, directories and personnal datas

app = Dash(__name__)


# -- Import and clean data (importing csv into pandas)
df_temperature = pd.read_csv(datas.database_folder_path + "temperatures_raspberry.csv")
df_temperature['datetime'] = pd.to_datetime(df_temperature['datetime'], format='mixed')
df_temperature.sort_values('datetime', inplace=True)
locations = df_temperature["location"].sort_values().unique()

df_daily_consumption = pd.read_csv(datas.database_folder_path + "daily_consumption.csv")
df_daily_consumption['date'] = pd.to_datetime(df_daily_consumption['date'], format='mixed')
df_daily_consumption.sort_values('date', inplace=True)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.Div(
        children=[
            html.P(children="🏠", className="header-emoji"),
            html.H1(children="House Monitoring", className="header-title"),
            html.P(
                children=(
                    "Analyze the temperatures"
                    " and the energy consumption"
                ),
                className="header-description",
            ),
        ],
        className="header",
    ),

    html.H2("Datas from Raspberry", style={'text-align': 'center'}),

    dcc.DatePickerRange(id="date-range-temperature",
                        display_format='DD/MM/YYYY',
                        min_date_allowed=df_temperature["datetime"].min().date(),
                        max_date_allowed=df_temperature["datetime"].max().date(),
                        start_date=datetime.today() - timedelta(days=7),
                        end_date=datetime.today(),
                        ),

    dcc.Graph(id='temperature_chart', figure={}),

    html.H2("Energy graphs", style={'text-align': 'center'}),

    dcc.DatePickerRange(id="date-range-energy",
                        display_format='DD/MM/YYYY',
                        min_date_allowed=df_daily_consumption['date'].min().date(),
                        max_date_allowed=df_daily_consumption['date'].max().date(),
                        start_date=df_daily_consumption['date'].max().date() - timedelta(days=7),
                        end_date=df_daily_consumption['date'].max().date(),
                        ),

    dcc.Graph(id='energy_chart', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='temperature_chart', component_property='figure'),
    Output(component_id='energy_chart', component_property='figure'),
    Input(component_id="date-range-temperature", component_property="start_date"),
    Input(component_id="date-range-temperature", component_property="end_date"),
    Input(component_id="date-range-energy", component_property="start_date"),
    Input(component_id="date-range-energy", component_property="end_date"),
)
def update_graph(start_date_temperature, end_date_temperature, start_date_energy, end_date_energy):

    # Update temperature graph
    dff_temperature = df_temperature.copy()
    dff_temperature = dff_temperature.loc[(dff_temperature['datetime'] > pd.to_datetime(start_date_temperature)) & (dff_temperature['datetime'] <= pd.to_datetime(end_date_temperature))]

    # Plotly Express
    fig_temperature = px.line(
        data_frame=dff_temperature,
        x="datetime",
        y="temperature",
        color="location",
        labels={
            "temperature": "Temperature (°C)",
            "datetime": "Date",
            "location": "Location:"
        },
        title="Temperatures by location",
    )

    # Update energy graph
    dff_energy = df_daily_consumption.copy()
    dff_energy = dff_energy.loc[(dff_energy['date'] > pd.to_datetime(start_date_energy)) & (dff_energy['date'] <= pd.to_datetime(end_date_energy))]

    # Plotly Express
    fig_energy = px.line(
        data_frame=dff_energy,
        x="date",
        y="value",
        labels={
            "daily consumption": "energy consumed (Wh)",
            "date": "Date",
        },
        title="Daily energy consumption",
    )

    return fig_temperature, fig_energy


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
