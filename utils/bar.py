import plotly.graph_objects as go

def plot(df, x, y, tooltip, color):
    traces = []

    df = df.sort_values(y, ascending=False)
    if color is not None:
        color_vals = df[color].unique().tolist()
    else:
        df["color"] = "color"
        color = "color"
        color_vals = ["color"]
    
    for color_val in color_vals:
        d = df[df[color]==color_val]
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
            go.Bar(
                x = d[x],
                y = d[y],
                name=color_val,
                hoverinfo="text",
                hovertext=tooltip_vals
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