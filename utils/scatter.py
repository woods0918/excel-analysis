import plotly.graph_objects as go

def plot(df, x, y, tooltip, size, color):
    traces = []
    if size is not None:
        df = _norm(df, size)

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
            go.Scatter(
                x = d[x],
                y = d[y],
                mode="markers",
                name=color_val,
                hoverinfo="text",
                hovertext=tooltip_vals,
                marker=dict(
                    size= 10 if size is None else d["norm"]
                )
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

def _norm(df, target_col):
    max_val = max(df[target_col])
    min_val = min(df[target_col])
    df["norm"] = ((df[target_col] - min_val) / (max_val - min_val)) * (50 - 5) + 5
    return df