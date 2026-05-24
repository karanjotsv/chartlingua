import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    name=''
))

title_text = texts.get('title')
if texts.get('subtitle'):
    title_text = f"{title_text}<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        font=dict(size=24)
    ),
    xaxis=dict(
        title=texts.get('x_axis_label'),
        type='category',
        showgrid=False,
        linecolor='black',
        ticks='outside'
    ),
    yaxis=dict(
        title=texts.get('y_axis_label'),
        range=[0, 35],
        tick0=0,
        dtick=5,
        gridcolor='lightgrey',
        linecolor='black',
        ticks='outside'
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=80, b=80, l=90, r=40)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")