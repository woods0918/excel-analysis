import os
import dash_html_components as html
import dash_bootstrap_components as dbc

def generate(class_name="header"):
    return dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/logo.png", height="40px"))
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/",
            )
        ],
        color="#ededed",
        dark=True,
        className=class_name
    )