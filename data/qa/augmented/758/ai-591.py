import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
output_image_path = os.path.splitext(json_file_path)[0] + ".png"

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else '#2a75d0',
    text=[f'{y}%' for y in y_values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

annotations = []
if texts.get('note'):
    annotations.append(dict(
        text=texts['note'],
        showarrow=False,
        xref="paper", yref="paper",
        x=0, y=-0.15,
        xanchor='left', yanchor='top'
    ))
if texts.get('source'):
    annotations.append(dict(
        text=texts['source'],
        showarrow=False,
        xref="paper", yref="paper",
        x=1, y=-0.15,
        xanchor='right', yanchor='top'
    ))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=70, r=30, b=100, t=30),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 41],
        tickformat='%g%%',
        dtick=5,
        gridcolor='#d3d3d3',
        zeroline=False,
        showline=False
    ),
    annotations=annotations
)

for year in range(min(x_values), max(x_values)):
    fig.add_vline(x=year + 0.5, line_width=1, line_color='#f0f0f0', layer='below')

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")