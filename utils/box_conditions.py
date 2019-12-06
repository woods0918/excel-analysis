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
                    id="box-x-dropdown",
                    options=[{"label": col, "value": col} for col in cols],
                    placeholder="選択してください"
                )
            ]),
            dbc.FormGroup([
                dbc.Label("Y軸(必須)", html_for="dropdown"),
                dcc.Dropdown(
                    id="box-y-dropdown",
                    options=[{"label": col, "value": col} for col in cols],
                    placeholder="選択してください"
                )
            ]),
            dbc.FormGroup([
                dbc.Label("ツールチップ(必須/複数選択可)", html_for="dropdown"),
                dcc.Dropdown(
                    id="box-tooltip-dropdown",
                    options=[{"label": col, "value": col} for col in cols],
                    placeholder="選択してください",
                    multi=True
                )
            ]),
            html.Div([
                dbc.Button("表示する", id="box-button", className="mr-1", color="success")
            ], className="box-button-area")
            
        ], className="box-conditions"),
        dcc.Graph(id="box-plot", figure=fig),
        html.A('HTML形式でグラフをダウンロード',
            id='box-download-link',
            download="chart.html",
            href="",
            target="_blank",
            style={"opacity": 0.0, "user-select": "none", "pointer-events": "none"}
        )
    ], className="box-area")