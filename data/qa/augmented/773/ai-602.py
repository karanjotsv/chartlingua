import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data to display in the same order as the image (top-to-bottom)
categories.reverse()
values.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors[0]),
    text=[f'{v:,}'.replace(',', ' ') for v in values],
    textposition='outside',
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(
        text=texts.get('title'),
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, max(values) * 1.18]
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        showline=False,
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=120, r=80, t=50, b=80),
    bargap=0.4,
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.12,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='grey')
        )
    ]
)

output_filename = json_file_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")