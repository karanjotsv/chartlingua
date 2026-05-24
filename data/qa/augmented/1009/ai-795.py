import sys
import json
import plotly.graph_objects as go
import pathlib

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
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
    text=y_values,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    marker_color=colors[0] if colors else '#1f77b4',
    cliponaxis=False,
    hoverinfo='none'
))

annotations = []
if texts.get('note'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0, y=-0.15,
        xanchor='left', yanchor='top',
        text=texts['note'],
        showarrow=False,
        font=dict(family="Arial", size=12)
    ))

if texts.get('source'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=1, y=-0.15,
        xanchor='right', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=12)
    ))


fig.update_layout(
    margin=dict(l=80, r=40, t=40, b=120),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial", size=12),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 7],
        tickmode='linear',
        tick0=0,
        dtick=1,
        gridcolor='#E5E5E5',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        type='category'
    ),
    annotations=annotations
)

output_path = pathlib.Path(json_path).with_suffix('.png')
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")