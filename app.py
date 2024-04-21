import inspect
import os
from datetime import datetime as dt
from datetime import timedelta

import common_modules
import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
from dash import dcc, html

app_path = inspect.getfile(inspect.currentframe())
dash_dir = os.path.realpath(os.path.dirname(app_path))

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
app.config.suppress_callback_exceptions = True

colors = {
    "background": "#f5f6f7",  # '#9KDBFF'
    "div_bg": "#9KDBFF",  ##e2ecfb
    "text": "#000000",
}

divBorder = {"border": "1px outset white", "border-radius": "5px"}


def myconverter(o):
    if isinstance(o, dt):
        return o.__str__()


app.layout = html.Div(
    style={"backgroundColor": colors["background"], "margin": "auto"},
    children=[
        html.Div(
            [
                common_modules.get_header(),
                common_modules.get_menu(),
            ],
            style={"backgroundColor": "#fcfcfc"},
        ),
        html.Br(),
        html.Div(
            [
                dcc.DatePickerRange(
                    id="my-date-picker-range",
                    min_date_allowed=dt(2019, 10, 31),
                    max_date_allowed=dt(2021, 12, 31),
                    initial_visible_month=dt(2020, 9, 1),
                    start_date=dt.today() - timedelta(days=8),
                    end_date=dt.today() - timedelta(days=1),
                ),
                html.Div(id="output-container-date-picker-range"),
                dcc.Loading(
                    html.Div(id="Intermediate-Details", style={"display": "none"}),
                    type="circle",
                ),
                html.Div(dcc.Store(id="Intermediate-Details1")),
            ]
        ),
        html.Br(),
        html.Div(
            [
                html.Div(
                    [
                        # unique creditors
                        html.Br(),
                        html.Div(
                            [
                                html.P("Creditors"),
                                html.H2(
                                    id="Unique-Credit",
                                    className="info_text",
                                    style={"textAlign": "center", "opacity": 5},
                                ),
                            ],
                            style={
                                "textAlign": "center",
                                "fontSize": 15,
                                "font-family": "Helvetica Neue, Helvetica, Arial",
                            },
                        ),
                        html.Br(),
                        html.Div(
                            [
                                html.P("Defaulters"),
                                html.H2(
                                    id="Defaulters",
                                    className="info_text",
                                    style={"textAlign": "center", "opacity": 5},
                                ),
                            ],
                            style={
                                "textAlign": "center",
                                "fontSize": 15,
                                "font-family": "Helvetica Neue, Helvetica, Arial",
                            },
                        ),
                        html.Br(),
                        html.Div(
                            [
                                html.P("Real Estate Loans"),
                                html.H2(
                                    id="RealEstate",
                                    className="info_text",
                                    style={"textAlign": "center", "opacity": 5},
                                ),
                            ],
                            style={
                                "textAlign": "center",
                                "fontSize": 15,
                                "font-family": "Helvetica Neue, Helvetica, Arial",
                            },
                        ),
                    ],
                    style={
                        "float": "left",
                        "width": "25%",
                        "backgroundColor": "ffffff",
                        "border": divBorder["border"],
                        "border-radius": divBorder["border-radius"],
                        "display": "inline-block",
                        "boxSizing": "border-box",
                        "box-shadow": "2px 2px 2px lightgrey",
                        "position": "relative",
                    },
                ),
                #### Creditors Age Range
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id="Age-Stats")),
                    ],
                    style={
                        "backgroundColor": colors["div_bg"],
                        "border": divBorder["border"],
                        "border-radius": divBorder["border-radius"],
                        "display": "inline-block",
                        "boxSizing": "border-box",
                        "float": "right",
                        "width": "73%",
                        "box-shadow": "2px 2px 2px lightgrey",
                        "position": "relative",
                    },
                ),
            ],
            style={"paddingBottom": "5", "overflow": "auto"},
        ),
        html.Br(),
        html.Div(
            [
                html.Div(
                    [
                        #### Dependents-Stats Details
                        html.Div(
                            [
                                dcc.Loading(dcc.Graph(id="Dependents-Stats")),
                            ],
                            style={
                                "backgroundColor": colors["div_bg"],
                                "border": divBorder["border"],
                                "border-radius": divBorder["border-radius"],
                                "display": "inline-block",
                                "boxSizing": "border-box",
                                "float": "left",
                                "width": "60%",
                                "box-shadow": "2px 2px 2px lightgrey",
                                "position": "relative",
                            },
                        ),
                        #### Income-Stats
                        html.Div(
                            [
                                dcc.Loading(dcc.Graph(id="Income-Stats")),
                            ],
                            style={
                                "backgroundColor": colors["div_bg"],
                                "border": divBorder["border"],
                                "border-radius": divBorder["border-radius"],
                                "display": "inline-block",
                                "boxSizing": "border-box",
                                "float": "right",
                                "width": "38%",
                                "box-shadow": "2px 2px 2px lightgrey",
                                "position": "relative",
                            },
                        ),
                    ],
                    style={"paddingBottom": "5", "overflow": "auto"},
                ),
            ]
        ),
    ],
    className="container",
)


############### DB Loader Articles
@app.callback(
    dash.dependencies.Output("Intermediate-Details1", "children"),
    [
        dash.dependencies.Input("my-date-picker-range", "start_date"),
        dash.dependencies.Input("my-date-picker-range", "end_date"),
    ],
)
def cred_data(start_date, end_date):
    credit_dataset = pd.read_csv("data/cs-training.csv")
    return credit_dataset.head(1000).to_dict()


############### Unique rated Articles
@app.callback(
    dash.dependencies.Output("Unique-Credit", "children"),
    [dash.dependencies.Input("Intermediate-Details1", "children")],
)
def unique_creditors(credit_dataset):
    credit_dataset = pd.DataFrame(credit_dataset)
    credit_data = credit_dataset[
        [
            "SeriousDlqin2yrs",
            "age",
            "DebtRatio",
            "MonthlyIncome",
            "NumberOfOpenCreditLinesAndLoans",
            "NumberRealEstateLoansOrLines",
            "NumberOfDependents",
        ]
    ]
    unique_credits = len(credit_data)

    return unique_credits


############### Unique Raters
@app.callback(
    dash.dependencies.Output("Defaulters", "children"),
    [dash.dependencies.Input("Intermediate-Details1", "children")],
)
def defaulters(credit_dataset):
    credit_dataset = pd.DataFrame(credit_dataset)
    credit_data = credit_dataset[
        [
            "SeriousDlqin2yrs",
            "age",
            "DebtRatio",
            "MonthlyIncome",
            "NumberOfOpenCreditLinesAndLoans",
            "NumberRealEstateLoansOrLines",
            "NumberOfDependents",
        ]
    ]

    defaulters = len(credit_data[credit_data["SeriousDlqin2yrs"] == 1])

    return defaulters


############### Real Estate Lons
@app.callback(
    dash.dependencies.Output("RealEstate", "children"),
    [dash.dependencies.Input("Intermediate-Details1", "children")],
)
def real_estate(credit_dataset):
    credit_dataset = pd.DataFrame(credit_dataset)
    credit_data = credit_dataset[
        [
            "SeriousDlqin2yrs",
            "age",
            "DebtRatio",
            "MonthlyIncome",
            "NumberOfOpenCreditLinesAndLoans",
            "NumberRealEstateLoansOrLines",
            "NumberOfDependents",
        ]
    ]

    real_estate = len(credit_data[credit_data["NumberRealEstateLoansOrLines"] > 0])

    return real_estate


############### Age Stats
@app.callback(
    dash.dependencies.Output("Age-Stats", "figure"),
    [dash.dependencies.Input("Intermediate-Details1", "children")],
)
def age_data(credit_dataset):
    credit_dataset = pd.DataFrame(credit_dataset)
    credit_data = credit_dataset[
        [
            "SeriousDlqin2yrs",
            "age",
            "DebtRatio",
            "MonthlyIncome",
            "NumberOfOpenCreditLinesAndLoans",
            "NumberRealEstateLoansOrLines",
            "NumberOfDependents",
        ]
    ]
    hist, bin_edges = np.histogram(credit_data.age, bins=10)

    data = plotly.graph_objs.Bar(
        x=bin_edges[:-1],
        y=hist,
        name="Age_Creditors",
    )

    return {
        "data": [data],
        "layout": go.Layout(
            title=dict(
                text="<b> Creditors' Age </b>",
            ),
            font=dict(size=10),
            height=350,
            margin=dict(l=120, r=50, b=50, t=100, pad=2),
            xaxis=dict(automargin=True, tickangle=45, title="age range"),
        ),
    }


############### Defaulter vs Dependents Stats


@app.callback(
    dash.dependencies.Output("Dependents-Stats", "figure"),
    [dash.dependencies.Input("Intermediate-Details1", "children")],
)
def defaulter_data(credit_dataset):
    credit_dataset = pd.DataFrame(credit_dataset)
    credit_data = credit_dataset[["SeriousDlqin2yrs", "NumberOfDependents"]]

    # Group data by Number of Dependents and calculate the count of SeriousDlqin2yrs
    grouped_data = (
        credit_data.groupby("NumberOfDependents")["SeriousDlqin2yrs"]
        .sum()
        .reset_index()
    )

    data = plotly.graph_objs.Scatter(
        x=grouped_data["NumberOfDependents"],
        y=grouped_data["SeriousDlqin2yrs"],
        mode="markers",
        marker=dict(size=10, color="blue", opacity=0.7),
        name="Number of Dependents vs Defaulters",
    )

    return {
        "data": [data],
        "layout": go.Layout(
            title=dict(
                text="<b>Number of Dependents vs Defaulters</b>",
            ),
            font=dict(size=10),
            height=350,
            margin=dict(l=120, r=50, b=50, t=100, pad=2),
            xaxis=dict(title="Number of Dependents"),
            yaxis=dict(title="Number of Defaulters"),
        ),
    }


############### Monthly Income Stats


@app.callback(
    dash.dependencies.Output("Income-Stats", "figure"),
    [dash.dependencies.Input("Intermediate-Details1", "children")],
)
def income_data(credit_dataset):
    if not credit_dataset:
        return {}

    credit_data = pd.DataFrame(credit_dataset)

    if "MonthlyIncome" not in credit_data.columns:
        return {}
    credit_data = credit_data[["MonthlyIncome"]]

    # Define income bins
    income_bins = [0, 2000, 4000, 6000, 8000, 10000, float("inf")]
    labels = [
        "0-2000",
        "2001-4000",
        "4001-6000",
        "6001-8000",
        "8001-10000",
        "Above 10000",
    ]

    # Categorize monthly income into bins
    credit_data["IncomeRange"] = pd.cut(
        credit_data["MonthlyIncome"], bins=income_bins, labels=labels, right=False
    )

    # Count the frequency of each income range
    income_counts = credit_data["IncomeRange"].value_counts()

    data = plotly.graph_objs.Pie(
        labels=income_counts.index,
        values=income_counts.values,
        hole=0.3,
        name="Monthly Income Distribution",
    )

    return {
        "data": [data],
        "layout": go.Layout(
            title=dict(
                text="<b>Monthly Income Distribution</b>",
            ),
            font=dict(size=10),
            height=400,
            margin=dict(l=50, r=50, b=100, t=100, pad=2),
        ),
    }


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
