import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = chart_data['categories']
series_data = chart_data['series']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series, preserving order
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=categories,
        y=series['values'],
        marker_color=colors[i % len(colors)] # Use modulo for color safety
    ))

# Build the title string
title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout for a professional look and to match the original
fig.update_layout(
    barmode='stack',
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font={
        'family': "Arial",
        'size': 12
    },
    legend={
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': -0.5, # Adjust position to avoid overlap with long x-axis labels
        'xanchor': 'center',
        'x': 0.5
    },
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis={
        'showgrid': False,
        'tickangle': 0
    },
    yaxis={
        'showgrid': True,
        'gridcolor': 'lightgrey',
        'range': [0, 60]
    },
    margin={
        'l': 60,
        'r': 30,
        't': 80,
        'b': 200 # Increased bottom margin for multi-line x-axis labels
    }
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")