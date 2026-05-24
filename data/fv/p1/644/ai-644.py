import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)]
    ))

fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(
        family="Arial",
        size=16
    ),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        type='category',
        showline=True,
        linecolor='black',
        linewidth=1,
        mirror=True,
        ticks='outside'
    ),
    yaxis=dict(
        range=[0, 120],
        tickmode='array',
        tickvals=[0, 20, 40, 60, 80, 100, 120],
        showgrid=True,
        gridcolor='grey',
        gridwidth=1,
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        mirror=True,
        ticks='outside'
    ),
    margin=dict(l=100, r=30, t=80, b=80)
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")