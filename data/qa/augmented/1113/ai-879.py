import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#1f77b4',
    text=values,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='black')
))

title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<span style='font-size: 18px;'><b>{title_text}</b></span>"
if subtitle_text:
    full_title += f"<br><span style='font-size: 14px;'>{subtitle_text}</span>"

annotations = []
source_text = texts.get('source')
if source_text:
    source_parts = source_text.split('<br>')
    if len(source_parts) > 0 and source_parts[0]:
        annotations.append(dict(
            text=source_parts[0],
            xref="paper", yref="paper",
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            showarrow=False,
            font=dict(family="Arial", size=12, color='#666666')
        ))
    if len(source_parts) > 1 and source_parts[1]:
        annotations.append(dict(
            text=source_parts[1],
            xref="paper", yref="paper",
            x=1, y=-0.15,
            xanchor='right', yanchor='top',
            showarrow=False,
            font=dict(family="Arial", size=12, color='#666666')
        ))

fig.update_layout(
    font=dict(family="Arial"),
    title=dict(text=full_title, x=0.05, xanchor='left'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        gridcolor='#EAEAEA',
        range=[0, 18],
        tickvals=[0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5],
        linecolor='black'
    ),
    margin=dict(l=80, r=40, t=60, b=100),
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")