import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#1f77b4',
    text=values,
    texttemplate='%{y:.2f}',
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='black'),
    cliponaxis=False
))

# Combine title and subtitle
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if subtitle_text:
    title_text = f"{title_text}<br><span style='font-size:0.8em;color:#666;'>{subtitle_text}</span>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 45],
        tickmode='linear',
        tick0=0,
        dtick=5,
        gridcolor='#e9e9e9',
        zeroline=True,
        zerolinecolor='#e9e9e9'
    ),
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='#666666')
        )
    ]
)

# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)