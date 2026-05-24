#!/usr/bin/env python
import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

output_path = json_path.with_suffix(".png")

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors['bar_color'],
    text=y_values,
    textposition='outside',
    textfont=dict(
        family='Arial',
        size=14,
        color=colors['data_label_color']
    ),
    cliponaxis=False,
    hoverinfo='none'
))

title_html = (
    f"<b style='font-size: 26px; color:{colors['title_color']};'>{texts['title']}</b>"
    f"<br><span style='font-size: 18px; color:{colors['subtitle_color']};'>{texts['subtitle']}</span>"
)

fig.update_layout(
    title=dict(
        text=title_html,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor=colors['axis_line_color'],
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        visible=False,
        range=[0, max(y_values) * 1.15] # Ensure space for text above the highest bar
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial"
    ),
    showlegend=False,
    margin=dict(t=100, b=50, l=40, r=40)
)

fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")