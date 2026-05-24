import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

base_name = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_name}.png"

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    texttemplate='%{y}',
    textposition='outside',
    hoverinfo='none',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

annotations = []
if texts.get('source'):
    annotations.append(
        go.layout.Annotation(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.22,
            xanchor='right',
            yanchor='top'
        )
    )
if texts.get('note'):
    annotations.append(
        go.layout.Annotation(
            text=texts['note'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.0,
            y=-0.22,
            xanchor='left',
            yanchor='top'
        )
    )

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        range=[0, 70],
        linecolor='black'
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=annotations
)

fig.write_image(output_image_path, scale=2)
print(f"Chart saved to {output_image_path}")