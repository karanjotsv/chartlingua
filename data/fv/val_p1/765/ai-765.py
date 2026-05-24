import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = Path(sys.argv[1])

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data for the chart
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly Pie chart
labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Replicate original chart's logic of hiding percentage for very small slices
text_labels = [f'{v}%' if v > 1 else '' for v in values]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1.5)
    ),
    text=text_labels,
    textinfo='text',
    textposition='inside',
    textfont=dict(family="Arial", size=20, color='black'),
    sort=False,
    direction='clockwise',
    rotation=180,
    showlegend=True
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Build the title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        color="white"
    ),
    legend=dict(
        traceorder='reversed'
    ),
    paper_bgcolor='black',
    plot_bgcolor='black',
    margin=dict(t=100, b=40, l=40, r=40)
)

# Determine output filename and save the image
output_filename = json_file_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")