import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False,
    textfont=dict(family="Arial", size=10, color='black')
))

layout_annotations = []
if texts.get("source"):
    layout_annotations.append(
        dict(
            x=1,
            y=-0.15,
            xref='paper',
            yref='paper',
            text=texts["source"],
            showarrow=False,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(family="Arial", size=12, color="grey")
        )
    )

fig.update_layout(
    title_text=texts.get("title"),
    yaxis_title_text=texts.get("y_axis_title"),
    xaxis_title_text=texts.get("x_axis_title"),
    font=dict(family="Arial"),
    showlegend=False,
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 2000],
        tickvals=[0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000],
        showgrid=True,
        gridcolor='lightgray',
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=layout_annotations
)

output_filename = json_path.with_suffix(".png").name
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")