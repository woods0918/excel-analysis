import os, time, flask, urllib, uuid
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

from app import app
from setting import RESOURCE_DIR
from utils import table, scatter, scatter_conditions, bar_conditions, bar, box_conditions, box
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
        dcc.Loading(id='tabs-content', type="default")
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
        return bar_conditions.plot(df, fig)
    elif tab == 'tab-box':
        return box_conditions.plot(df, fig)

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
    
    if size is not None:
        try:
            data[size] = data[size].fillna(0.0).astype("float")
        except:
            size = None
        
    return scatter.plot(data, x, y, tooltip, size, color)

@app.callback(
    Output("bar-plot", "figure"),
    [
        Input("bar-button", "n_clicks")
    ],
    [
        State("bar-x-dropdown", "value"),
        State("bar-y-dropdown", "value"),
        State("bar-tooltip-dropdown", "value"),
        State("bar-color-dropdown", "value"),
        State("upload-data-store", "data")
    ]
)
def plot_bar(n_clicks, x, y, tooltip, color, data):
    data = pd.DataFrame(data)
    if x is None or y is None or tooltip is None:
        raise PreventUpdate

    if data is None:
        raise PreventUpdate

    try:
        data[y] = data[y].fillna(0.0).astype('float')
    except Exception as e:
        print(e)
        raise PreventUpdate
        
    return bar.plot(data, x, y, tooltip, color)

@app.callback(
    Output("box-plot", "figure"),
    [
        Input("box-button", "n_clicks")
    ],
    [
        State("box-x-dropdown", "value"),
        State("box-y-dropdown", "value"),
        State("box-tooltip-dropdown", "value"),
        State("upload-data-store", "data")
    ]
)
def plot_box(n_clicks, x, y, tooltip, data):
    data = pd.DataFrame(data)
    if x is None or y is None or tooltip is None:
        raise PreventUpdate

    if data is None:
        raise PreventUpdate

    try:
        data[y] = data[y].fillna(0.0).astype('float')
    except Exception as e:
        print(e)
        raise PreventUpdate
        
    return box.plot(data, x, y, tooltip)

def update_download_link(figure, href):
    if os.path.exists(os.path.join(RESOURCE_DIR, href.replace("/downloads/", ""))):
        os.remove(os.path.join(RESOURCE_DIR, href.replace("/downloads/", "")))

    if len(figure["data"]) == 0:
        raise PreventUpdate
    
    filename = f"{uuid.uuid1()}.html"
    filepath = os.path.join(RESOURCE_DIR, filename)
    chart_output(figure, filepath)
    
    return "/downloads/" + filename

def link_style(n_clicks, x, y, tooltip, data):
    if x is None or y is None or tooltip is None:
        return {"opacity": 0.0, "user-select": "none", "pointer-events": "none"}

    if data is None:
        return {"opacity": 0.0, "user-select": "none", "pointer-events": "none"}
    
    return {"font-size":"14px"}

for plot_type in ["scatter", "tab", "box"]:
    app.callback(
        Output(f'{plot_type}-download-link', 'href'),
        [Input(f"{plot_type}-plot", "figure")],
        [State(f'{plot_type}-download-link', 'href')]
    )(update_download_link)

    app.callback(
        Output(f"{plot_type}-download-link", "style"),
        [
            Input(f"{plot_type}-button", "n_clicks")
        ],
        [
            State(f"{plot_type}-x-dropdown", "value"),
            State(f"{plot_type}-y-dropdown", "value"),
            State(f"{plot_type}-tooltip-dropdown", "value"),
            State("upload-data-store", "data")
        ]
    )(link_style)

@app.server.route('/downloads/<path:path>')
def serve_static(path):
    return flask.send_from_directory(
        RESOURCE_DIR, path
    )