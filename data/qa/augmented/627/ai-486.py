import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for plotting, reversing order for top-to-bottom display in Plotly
categories = [item['category'] for item in data][::-1]
values = [item['value'] for item in data][::-1]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0],
    text=[f'{v:,}'.replace(',', ' ') for v in values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

# Build title and source strings
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = ""
if texts.get('source'):
    source_text += texts['source']
if texts.get('note'):
    source_text += f"<br>{texts['note']}"

fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=150, r=60, t=50, b=80),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        range=[0, 14000],
        dtick=2000
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks=''
    ),
    showlegend=False
)

if source_text:
    fig.add_annotation(
        text=source_text,
        align='right',
        showarrow=False,
        xref='paper', yref='paper',
        x=1, y=-0.15,
        xanchor='right', yanchor='top',
        font=dict(family="Arial", size=10, color='#666666')
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")