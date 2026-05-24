import sys
import json
import os
import plotly.graph_objects as go

# Read chart data from the JSON file provided as a command-line argument
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts from the loaded JSON
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = chart_data['categories']
series_data = chart_data['series']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series, iterating to preserve order
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=categories,
        y=series['data'],
        marker_color=colors[i],
        text=[f"{val}%" for val in series['data']],
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        hoverinfo='none'
    ))

# Combine title and subtitle using HTML for formatting
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>" if full_title else f"<sub>{subtitle_text}</sub>"

# Update the figure layout
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 105],
        tickvals=[0, 20, 40, 60, 80, 100],
        ticktext=[f"{v}%" for v in [0, 20, 40, 60, 80, 100]],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=70, r=30, b=140, t=50)
)

# Add source text as an annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.35,
        font=dict(size=10)
    )

# Derive output filename from the input JSON file path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")