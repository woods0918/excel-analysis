import dash, flask, os
import dash_bootstrap_components as dbc

from setting import APP_TITLE

# --------------------------------------------
# Generate Dash application
# --------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config['suppress_callback_exceptions'] = True
app.title = APP_TITLE

server = app.server
server.route('/')
def favicon():
    return flask.send_from_directory(os.path.join(server.root_path, 'assets'),'favicon.ico')