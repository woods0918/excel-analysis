import plotly.graph_objects as go

def plot(df, x, y, tooltip):
    traces = []

    x_vals = df[x].unique().tolist()

    for x_val in x_vals:
        d = df[df[x]==x_val]
        tooltip_vals = []
        for i in range(len(d)):
            tooltip_val = ""
            for j, val in enumerate(tooltip):
                if j == 0:
                    tooltip_val += f"{val}: {d.iloc[i][val]}"
                else:
                    tooltip_val += f"<br>{val}: {d.iloc[i][val]}"
            tooltip_vals.append(tooltip_val)

        traces.append(
            go.Box(
                y = d[y],
                name = x_val,
                marker=dict(
                    size=2
                ),
                line=dict(
                    width=1
                ),
                boxpoints = "all",
                hoverinfo = "text",
                text = tooltip_vals,
                jitter = 0.5,
                whiskerwidth = 0.2
                )
            )
    
    layout = go.Layout(
        width=1400,
        height=600,
        legend_orientation="h",
        hovermode= 'closest',
        xaxis = dict(
            title=x
        ),
        yaxis = dict(
            title=y
        )
    )

    return dict(data = traces, layout = layout)