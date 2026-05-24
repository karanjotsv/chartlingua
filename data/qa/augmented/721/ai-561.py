import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Create the figure object
fig = go.Figure()

# Extract data for convenience
chart_data = chart_config.get('chart_data', [])
categories = chart_config.get('categories', [])
colors = chart_config.get('colors', [])
texts = chart_config.get('texts', {})

# Add bar traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('values', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=series.get('values', []),
        texttemplate='%{y:.2f}',
        textposition='outside',
        textfont=dict(size=11, color='black')
    ))

# Build title string
title_text = ""
if texts.get('title'):
    title_text += texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Create annotations for source and note
annotations = []
if texts.get('note'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.3,
            xanchor='left', yanchor='bottom',
            text=texts['note'],
            showarrow=False,
            font=dict(size=12)
        )
    )
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.3,
            xanchor='right', yanchor='bottom',
            text=texts['source'],
            showarrow=False,
            font=dict(size=12)
        )
    )

# Update layout
fig.update_layout(
    barmode='group',
    font_family="Arial",
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1050],
        dtick=200,
        showgrid=True,
        gridcolor='#e0e0e0'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    margin=dict(l=80, r=40, t=50, b=150),
    annotations=annotations
)

# Define output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)