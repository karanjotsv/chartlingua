import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}", file=sys.stderr)
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    showlegend=False
))

fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    font=dict(
        family="Arial"
    ),
    xaxis_title_text=texts.get('x_axis_title'),
    yaxis_title_text=texts.get('y_axis_title'),
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='lightgrey'
    ),
    yaxis=dict(
        range=[0, 60],
        dtick=10,
        showgrid=True,
        gridcolor='lightgrey',
        showline=False
    ),
    margin=dict(t=80, b=80, l=60, r=40)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)