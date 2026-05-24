import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {Path(sys.argv[0]).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

output_path = json_path.with_suffix(".png")

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for series, color in zip(chart_data, colors):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=color),
        marker=dict(
            color=color,
            symbol=series['marker_symbol'],
            size=8,
            line=dict(width=1, color='Black') # Markers in original have black outlines
        )
    ))

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.04,
        xanchor='left',
        font=dict(size=16)
    ),
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=False,
        dtick=2,
        tickmode='linear'
    ),
    yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=False,
        range=[0, 600],
        dtick=100,
        zeroline=False
    ),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bordercolor='black',
        borderwidth=1,
        bgcolor='rgba(255,255,255,0.8)'
    ),
    margin=dict(l=80, r=40, t=80, b=80)
)

fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")