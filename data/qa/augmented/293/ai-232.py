import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
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

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', {})

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors.get('primary', ['#367AC1'])[0],
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False,
    textfont=dict(family='Arial', size=12, color='black')
))

title_parts = []
if texts.get('title'):
    title_parts.append(texts['title'])
if texts.get('subtitle'):
    title_parts.append(f"<span style='font-size:0.8em'>{texts['subtitle']}</span>")
title_text = "<br>".join(title_parts)

annotations = []
if texts.get('note'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0, y=-0.2,
        xanchor='left', yanchor='top',
        text=texts['note'],
        showarrow=False,
        font=dict(family='Arial', size=12, color='#0073B2'),
        align='left'
    ))
if texts.get('source'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=1, y=-0.2,
        xanchor='right', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(family='Arial', size=12, color='#666666'),
        align='right'
    ))

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left',
        font=dict(family='Arial')
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='lightgrey',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 15],
        tickvals=[0, 2.5, 5, 7.5, 10, 12.5, 15],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        showline=False,
        tickfont=dict(size=12)
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=annotations
)

fig.write_image(output_filename, scale=2)

print(f"Image saved to {output_filename}")