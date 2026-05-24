import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [d['category'] for d in data]
values = [d['value'] for d in data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    texttemplate='%{label} %{value}%',
    textposition='outside',
    sort=False,
    direction='clockwise',
    hovertemplate='%{label}: %{value}%<extra></extra>'
))

title_text = texts.get('title')
source_text = texts.get('source')

fig.update_layout(
    title_text=f"<b>{title_text}</b>" if title_text else None,
    title_x=0.5,
    font_family="Arial",
    font_size=14,
    showlegend=False,
    margin=dict(l=80, r=80, t=80, b=80),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0.99, y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=10, color="grey")
    )

base_name = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")