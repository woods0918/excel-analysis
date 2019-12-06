import os, time, flask
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from datetime import datetime

from app import app
from setting import RESOURCE_DIR
from utils import table, scatter, scatter_conditions
from utils.plot_tools import chart_output

tabs_styles = {
    'height': '44px',
    'width': '80vw'
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#4CAF50',
    'color': 'white',
    'padding': '6px'
}

fig = go.Figure(data=[],layout=go.Layout(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False
    ),  
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False
    )
))

def generate(class_name):
    return html.Div([
        dcc.Tabs(id="tabs", value='tab-table', children=[
            dcc.Tab(label='テーブル', value='tab-table', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='散布図', value='tab-scatter', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='棒グラフ', value='tab-line', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='はこひげ図', value='tab-box', style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),
        dcc.Loading(id='tabs-content', type="default"),
        html.A('HTML形式でグラフをダウンロード',
            id='download-link',
            href="",
            target="_blank",
            style={"opacity": 0.0, "user-select": "none", "pointer-events": "none"}
        )
    ], className=class_name)

@app.callback(
    Output('tabs-content', 'children'),
    [
        Input('tabs', 'value')
    ],
    [
        State("upload-data-store", "data")
    ]
)
def render_content(tab, df):
    if tab is None:
        raise PreventUpdate
    
    if df is None:
        return "データのアップロードに失敗しました。もう一度ファイルのアップロードをやり直してください"
    
    df = pd.DataFrame(df)

    if tab == 'tab-table':
        return table.plot(df, "table-plot")
    elif tab == 'tab-scatter':
        return scatter_conditions.plot(df, fig)
    elif tab == 'tab-line':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif tab == 'tab-box':
        return html.Div([
            html.H3('Tab content 4')
        ])

@app.callback(
    Output("scatter-plot", "figure"),
    [
        Input("scatter-button", "n_clicks")
    ],
    [
        State("scatter-x-dropdown", "value"),
        State("scatter-y-dropdown", "value"),
        State("scatter-tooltip-dropdown", "value"),
        State("scatter-size-dropdown", "value"),
        State("scatter-color-dropdown", "value"),
        State("upload-data-store", "data")
    ]
)
def plot_scatter(n_clicks, x, y, tooltip, size, color, data):
    data = pd.DataFrame(data)
    if x is None or y is None or tooltip is None:
        raise PreventUpdate

    if data is None:
        raise PreventUpdate

    try:
        data[x] = data[x].fillna(0.0).astype('float')
        data[y] = data[y].fillna(0.0).astype('float')
    except Exception as e:
        print(e)
        raise PreventUpdate
        
    return scatter.plot(data, x, y, tooltip, size, color)

@app.callback(
    Output("download-link", "style"),
    [
        Input("scatter-button", "n_clicks")
    ],
    [
        State("scatter-x-dropdown", "value"),
        State("scatter-y-dropdown", "value"),
        State("scatter-tooltip-dropdown", "value"),
        State("scatter-size-dropdown", "value"),
        State("scatter-color-dropdown", "value"),
        State("upload-data-store", "data")
    ]
)
def link_style(n_clicks, x, y, tooltip, size, color, data):
    if x is None or y is None or tooltip is None:
        return {"opacity": 0.0, "user-select": "none", "pointer-events": "none"}

    if data is None:
        return {"opacity": 0.0, "user-select": "none", "pointer-events": "none"}
    
    return {"font-size":"14px"}

@app.callback(Output('download-link', 'href'),
    [
        Input("scatter-plot", "figure")
    ],
    [
        State('download-link', 'href')
    ]
)
def update_download_link(figure, href):

    if os.path.exists(href):
        os.remove(href)
    if len(figure["data"]) == 0:
        raise PreventUpdate

    filepath = os.path.join(RESOURCE_DIR, f"{datetime.now()}.html")
    chart_output(figure, filepath)
    print(filepath)
    return filepath

@app.server.route('/resources/<path:path>')
def serve_static(path):
    print(path)
    root_dir = os.getcwd()
    return flask.send_from_directory(
        os.path.join(root_dir, 'resources'), path
    )

if __name__ == '__main__':
    app.run_server(debug=True)

def build_download_button(uri):
    button = html.Form(
        action=uri,
        method="get",
        children=[
            html.Button(
                className="button",
                type="submit",
                children=[
                    "download"
                ]
            )
        ]
    )
    return button