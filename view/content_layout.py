
# import external packages
from dash import dcc, html
import pandas as pd

# import project packages
import helpers.datas as datas


data = (
    pd.read_csv(datas.database_folder_path + "temperatures_raspberry.csv")
    # .query("type == 'conventional' and region == 'Albany'")
    .assign(Date=lambda data: pd.to_datetime(data["datetime"], format='mixed'))
    .sort_values(by="datetime")
)


content_layout = [
    html.Div(
        children=[
            html.H1(children="Home dashboard", className="header-title"),
            html.P(
                children=(
                    "Analyze the temperatures"
                    " and energy consumption."
                ),
            ),
            dcc.Graph(
                figure={
                    "data": [
                        {
                            "x": data["datetime"],
                            "y": data["temperature"],
                            "type": "lines",
                        },
                    ],
                    "layout": {"title": "Temperature"},
                },
            ),
            dcc.Graph(
                figure={
                    "data": [
                        {
                            "x": data["datetime"],
                            "y": data["temperature"],
                            "type": "lines",
                        },
                    ],
                    "layout": {"title": "Temperature"},
                },
            ),
        ]
    )
]
