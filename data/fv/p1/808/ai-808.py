import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=chart_data['categories'],
        y=series['data'],
        marker_color=colors[i]
    ))

fig.update_layout(
    barmode='stack',
    title={
        'text': texts['title'],
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis={
        'title_text': texts['x_axis_title'],
        'tickangle': 0,
        'showline': False
    },
    yaxis={
        'title_text': texts['y_axis_title'],
        'range': [0, 60],
        'showline': False,
        'gridcolor': '#e0e0e0'
    },
    legend={
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': -0.6,
        'xanchor': 'center',
        'x': 0.5
    },
    font={
        'family': "Arial",
        'size': 12
    },
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=80, b=220)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")