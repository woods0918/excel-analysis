from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from app import app, server
from components import header, footer
from apps import analysis, top

app.layout = html.Div([
    dcc.Store(id="upload-data-store", storage_type='session'),
    header.generate(),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-component'),
    footer.generate()
], className="root")

@app.callback(
    Output('page-component', 'children'),
    [
        Input('url', 'pathname')
    ])
def display_app(pathname):
    if pathname == '/':
        return top.generate(class_name="top-page")
    elif pathname == "/analysis":
        return analysis.generate(class_name="analysis-page")
    else:
        return top.generate(class_name="top-page")

if __name__ == "__main__":
    app.run_server(debug=False, port=8080)