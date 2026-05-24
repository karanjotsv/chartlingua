import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

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

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None,
        text=series.get('y'),
        textposition='outside',
        cliponaxis=False,
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    ))

title_text = texts.get('title', '') or ''
if texts.get('subtitle'):
    title_text = f"<b>{title_text}</b><br>{texts.get('subtitle')}" if title_text else f"<b>{texts.get('subtitle')}</b>"

fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.05,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        type='category',
        showgrid=False,
        tickfont=dict(family="Arial")
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 370],
        showgrid=True,
        gridcolor='#e0e0e0',
        tickfont=dict(family="Arial")
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100)
)

source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0.99, y=-0.18,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(family="Arial", size=10, color='#666666')
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")