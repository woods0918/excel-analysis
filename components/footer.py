import dash_html_components as html

def generate(class_name="footer"):
    return html.Footer([
        "2019 Excel Analysis sample footer"
    ], className=class_name)