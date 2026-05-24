import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])
paper_bgcolor = config.get('paper_bgcolor', 'white')

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=1)
    ),
    texttemplate='%{value:.1f}%',
    textposition='outside',
    sort=False,
    direction='clockwise',
    hoverinfo='label+percent'
)

layout = go.Layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center',
        y=0.95,
        yanchor='top',
        font=dict(size=22)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(t=120, b=120, l=40, r=40),
    paper_bgcolor=paper_bgcolor,
    plot_bgcolor=paper_bgcolor
)

fig = go.Figure(data=[pie_trace], layout=layout)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")