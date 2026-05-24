import sys
import os
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get("chart_data", [])
categories = config.get("categories", [])
texts = config.get("texts", {})
colors = config.get("colors", [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series.get("name"),
        x=categories,
        y=series.get("y"),
        marker_color=colors[i % len(colors)]
    ))

annotations = []
if texts.get("source"):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1, y=-0.40,
            xanchor="right", yanchor="bottom",
            text=texts["source"],
            showarrow=False,
            font=dict(size=12, color="#666666")
        )
    )

fig.update_layout(
    barmode='group',
    xaxis_title=texts.get("x_axis_title"),
    yaxis_title=texts.get("y_axis_title"),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=30, b=150, t=50),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 35],
        gridcolor='#e0e0e0',
        gridwidth=1,
        showline=True,
        linewidth=1,
        linecolor='black',
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_png_path = f"{base_filename}.png"
fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")