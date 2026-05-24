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
    text=values,
    textposition='outside',
    texttemplate='%{y:d}',
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=60, b=100),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 12500],
        tickvals=[0, 2500, 5000, 7500, 10000, 12500],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        separatethousands=True
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False,
        tickangle=0
    )
)

fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig.update_yaxes(showline=True, linewidth=1, linecolor='black')

annotations = []
if texts.get('source_text'):
    annotations.append(
        dict(
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            text=texts.get('source_text'),
            showarrow=False,
            align='right',
            font=dict(size=12)
        )
    )

fig.update_layout(annotations=annotations)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")