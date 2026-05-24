import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
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
    y=categories[::-1],
    x=values[::-1],
    orientation='h',
    marker_color=colors[0] if colors else '#2A7FDD',
    text=values[::-1],
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='black'),
    cliponaxis=False
))

title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    title={
        'text': title_text,
        'x': 0.05,
        'xanchor': 'left'
    },
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        range=[0, max(values) * 1.18]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=True,
        linewidth=1.5,
        linecolor='black'
    ),
    margin=dict(l=350, r=40, t=50, b=80),
)

if texts.get('source'):
    fig.add_annotation(
        text=texts.get('source'),
        xref="paper", yref="paper",
        x=0.99, y=-0.15,
        xanchor='right', yanchor='top',
        showarrow=False,
        font=dict(family="Arial", size=12)
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")