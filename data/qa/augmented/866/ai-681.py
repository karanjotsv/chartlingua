import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False,
    texttemplate='%{y:,.1f}'.replace('.0', '')
))

title_text = texts.get('title')
if title_text:
    subtitle_text = texts.get('subtitle')
    if subtitle_text:
        title_text = f"<b>{title_text}</b><br>{subtitle_text}"

fig.update_layout(
    title_text=title_text,
    xaxis_title_text=texts.get('x_axis_title'),
    yaxis_title_text=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    yaxis=dict(
        range=[0, 6300],
        tickvals=[0, 1000, 2000, 3000, 4000, 5000, 6000],
        ticktext=['0', '1 000', '2 000', '3 000', '4 000', '5 000', '6 000'],
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False
    ),
    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=50, b=100)
)

source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.15,
        xanchor='left',
        yanchor='top'
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")