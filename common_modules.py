import base64
import inspect
import os

from dash import dcc as dcc
from dash import html

app_path = inspect.getfile(inspect.currentframe())
dash_dir = os.path.realpath(os.path.dirname(app_path))
dir_path = os.path.dirname(dash_dir)


encoded_image = base64.b64encode(open("img/image.jpg", "rb").read())


def get_header():
    header = html.Div(
        [
            html.Img(
                src="data:image/png;base64,{}".format(encoded_image.decode()),
                style={
                    "textAlign": "left",
                    "height": "40%",
                    "width": "20%",
                    "padding-top": 0,
                    "padding-right": 0,
                    "line-height": "1",
                    "margin-bottom": "0.85rem",
                    "margin-left": "1.25rem",
                    "margin-top": "0.75rem",
                    "fontColor": "#515151",
                },
            ),
            html.Br(),
            html.Br(),
        ],
        className="row gs-header gs-text-header",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link("Home", href="/", className="p-2 text-dark"),
            dcc.Link("CreditHistory   ", href="/", className="p-2 text-dark"),
        ],
        className="d-flex flex-column "
        "flex-md-row align-items-center "
        "p-1 px-md-4 mb-3 bg-white border-bottom ",
    )
    return menu
