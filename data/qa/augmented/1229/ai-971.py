import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
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
categories = texts.get('categories', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('y', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)]
    ))

title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=True,
        zerolinecolor='lightgrey',
        zerolinewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        ticksuffix='%',
        gridcolor='#e0e0e0',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        range=[-35, 45]
    ),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.2,
        xanchor='center',
        x=0.5
    ),
    plot_bgcolor='white',
    margin=dict(l=60, r=40, t=40, b=150),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.3,
            xanchor='left',
            yanchor='top',
            font=dict(size=10, color='grey')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")