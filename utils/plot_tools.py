import plotly.offline as offline

def chart_output(fig, output_path):
    offline.plot(
        fig,
        show_link = False,
        config={
            "displaylogo":False
        },
        filename=output_path,
        auto_open=False
    )