import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = chart_data.get('categories', [])
series_list = chart_data.get('series', [])

fig = go.Figure()

for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        name=series.get('name'),
        x=categories,
        y=series.get('data', []),
        marker_color=colors[i % len(colors)] if colors else None
    ))

title_text = texts.get('title', '')

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    barmode='group',
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    yaxis={
        'range': [0, 35],
        'ticksuffix': '%',
        'gridcolor': '#E0E0E0',
        'zeroline': False
    },
    xaxis={
        'gridcolor': '#E0E0E0'
    },
    legend={
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': -0.3,
        'xanchor': 'center',
        'x': 0.5
    },
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=80, b=100)
)

base_filename, _ = os.path.splitext(os.path.basename(json_path))
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")