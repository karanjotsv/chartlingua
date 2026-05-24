import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

chart_data = chart_json.get("chart_data", [])
texts = chart_json.get("texts", {})
colors = chart_json.get("colors", {})
series_colors = colors.get("series_colors", [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        name=series.get("name"),
        mode='lines',
        line=dict(
            color=series_colors[i % len(series_colors)] if series_colors else None,
            width=3
        )
    ))

annotations = []
if "annotations" in texts:
    for ann in texts["annotations"]:
        annotations.append(
            dict(
                x=ann.get("x"),
                y=ann.get("y"),
                text=ann.get("text"),
                showarrow=False,
                xanchor='left',
                yanchor='middle',
                align=ann.get("align", "left"),
                font=dict(family="Arial", size=12)
            )
        )

fig.update_layout(
    title=dict(
        text=texts.get("title"),
        x=0.5,
        xanchor='center',
        font=dict(family="Arial", size=20)
    ),
    xaxis=dict(
        title=texts.get("x_axis_title"),
        tickvals=[3, 6, 9, 12],
        range=[0, 14],
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        title=texts.get("y_axis_title"),
        range=[-4.0, 3.0],
        tickvals=[-4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0],
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=True,
        zerolinecolor='lightgrey',
        showline=True,
        linecolor='black',
        mirror=True
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=150, t=100, b=80),
    annotations=annotations
)

output_filename = json_path.with_suffix(".png")
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")