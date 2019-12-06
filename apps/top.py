import pandas as pd
import base64, io
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash_core_components as dcc

from app import app
from setting import APP_TITLE

def generate(class_name):
    return html.Div([
        dbc.Jumbotron([
            dbc.Container([
                html.H1(APP_TITLE, className="display-3"),
                html.P(
                    "誰でもExcelを簡単に分析できるサービスです"
                )
            ])
        ], className="top-message-area"),
        html.Div([
            dcc.Upload(
                id='upload-file',
                children=html.Div([
                    'ドラッグ&ドロップ or ',
                    html.A('ファイルを選択してください')
                ]),
                style={
                    'width': '100%',
                    'height': '100px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=False
            ),
            html.Div(id='output-data-upload'),
        ], className="top-upload-area"),
        html.Div([
            dcc.Link(dbc.Button("分析を開始する", id="analysis-button", className="mr-1", color="success"),href="./analysis")
        ], className="top-button-area")
    ], className=class_name)

@app.callback(
    Output("output-data-upload", "children"),
    [
        Input("upload-file", "contents")
    ],
    [
        State("upload-file", "filename")
    ]
)
def check_filename(contents, filename):
    if contents is None:
        return "ファイルが選択されていません"
    return filename

@app.callback(
    Output("upload-data-store", "data"),
    [
        Input("upload-file", "contents")
    ],
    [
        State("upload-file", "filename")
    ]
)
def start_analysis(contents, filename):
    if contents is None:
        return None

    df = parse(contents, filename)
    if df is None:
        return None
    
    return df.to_dict()

def parse(contents, filename):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            return pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename or 'xlsx' in filename:
            return pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return None