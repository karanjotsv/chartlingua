import sys
import json
import os
import plotly.graph_objects as go

# Load data from JSON file provided as a command-line argument
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_details = json.load(f)

# Extract data and settings from the JSON structure
chart_data_list = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

# Create figure
fig = go.Figure()

# Add bar traces for each data series
for i, series in enumerate(chart_data_list):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None
    ))

# Construct title and subtitle string
title_text = ""
if texts.get('title'):
    title_text += texts.get('title')
if texts.get('subtitle'):
    title_text += f"<br><span style='font-size:0.8em;color:#666666;'>{texts.get('subtitle')}</span>"

# Update layout for aesthetics and accuracy
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    title_text=title_text if title_text else None,
    title_x=0.05,
    title_y=0.95,
    title_xanchor='left',
    title_yanchor='top',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        ticks="",
        tickfont=dict(size=16)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        gridcolor='#E0E0E0',
        gridwidth=1,
        zeroline=False,
        range=[28000, 35000],
        dtick=1000,
        tickformat=',d',
        tickfont=dict(size=16),
        showline=False,
        ticks="outside",
        ticklen=5
    ),
    margin=dict(l=80, r=20, t=40, b=40)
)

# Construct and add source/note annotation if present
annotation_text_parts = []
if texts.get('source'):
    annotation_text_parts.append(texts.get('source'))
if texts.get('note'):
    annotation_text_parts.append(texts.get('note'))
annotation_text = "<br>".join(annotation_text_parts)

if annotation_text:
    fig.add_annotation(
        text=annotation_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.0,
        y=-0.15,
        xanchor='left',
        yanchor='top',
        font=dict(size=12, color="#666666")
    )

# Determine output filename from JSON path and save the image
base_name = os.path.basename(json_path)
output_filename = os.path.splitext(base_name)[0] + '.png'
fig.write_image(output_filename, scale=2)