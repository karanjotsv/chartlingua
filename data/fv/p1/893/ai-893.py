import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data for the chart
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=2)
    ),
    textinfo='value',
    texttemplate='%{value}%',
    hoverinfo='label+percent',
    sort=False,  # Preserve the original order from JSON
    direction='clockwise',
    textfont=dict(size=12, family="Arial", color='white')
)

# Construct title
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts['subtitle']}"

# Configure the layout
layout = go.Layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    font=dict(family="Arial", size=12),
    showlegend=True,
    legend=dict(
        x=0.9,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        bgcolor='rgba(255, 255, 255, 0.5)'
    ),
    margin=dict(l=50, r=400, t=100, b=50), # Increased right margin for legend
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Create the figure
fig = go.Figure(data=[pie_trace], layout=layout)

# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)