import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

def plot(df, fig):
    cols = df.columns.tolist()
    return html.Div([
        html.Div([
            dbc.FormGroup([
                dbc.Label("X軸(必須)", html_for="dropdown"),
                dcc.Dropdown(
                    id="scatter-x-dropdown",
                    options=[{"label": col, "value": col} for col in cols],
                    placeholder="選択してください"
                )
            ]),
            dbc.FormGroup([
                dbc.Label("Y軸(必須)", html_for="dropdown"),
                dcc.Dropdown(
                    id="scatter-y-dropdown",
                    options=[{"label": col, "value": col} for col in cols],
                    placeholder="選択してください"
                )
            ]),
            dbc.FormGroup([
                dbc.Label("ツールチップ(必須/複数選択可)", html_for="dropdown"),
                dcc.Dropdown(
                    id="scatter-tooltip-dropdown",
                    options=[{"label": col, "value": col} for col in cols],
                    placeholder="選択してください",
                    multi=True
                )
            ]),
            dbc.FormGroup([
                dbc.Label("サイズ", html_for="dropdown"),
                dcc.Dropdown(
                    id="scatter-size-dropdown",
                    options=[{"label": col, "value": col} for col in cols],
                    placeholder="選択してください"
                )
            ]),
            dbc.FormGroup([
                dbc.Label("色分け", html_for="dropdown"),
                dcc.Dropdown(
                    id="scatter-color-dropdown",
                    options=[{"label": col, "value": col} for col in cols],
                    placeholder="選択してください"
                )
            ]),
            html.Div([
                dbc.Button("表示する", id="scatter-button", className="mr-1", color="success")
            ], className="scatter-button-area")
            
        ], className="scatter-conditions"),
        dcc.Graph(id="scatter-plot", figure=fig),
        html.A('HTML形式でグラフをダウンロード',
            id='scatter-download-link',
            download="chart.html",
            href="",
            target="_blank",
            style={"opacity": 0.0, "user-select": "none", "pointer-events": "none"}
        )
    ], className="scatter-area")