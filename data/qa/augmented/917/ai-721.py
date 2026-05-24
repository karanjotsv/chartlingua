import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    texttemplate='%{y:.2f}%',
    textposition='outside',
    hoverinfo='none',
    showlegend=False
))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#f0f0f0',
        linecolor='black',
        showline=True,
        ticks='outside',
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 3],
        dtick=0.5,
        ticksuffix='%',
        tickformat='g',
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
    ),
    margin=dict(l=90, r=40, t=60, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.18,
            xanchor='right',
            yanchor='top'
        )
    ]
)

output_filename = json_file_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")