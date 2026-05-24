import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# --- 2. Prepare Data for Plotly ---
# Extract categories and values, preserving the original order
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create the Chart Figure ---
fig = go.Figure()

# Add the bar trace using the first (and only) color
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    name='' # Hide trace name from hover
))

# --- 4. Configure Layout and Styling ---
# Combine title and subtitle using HTML for flexible formatting
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    # Chart Title
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.05,
        'xanchor': 'left',
        'yanchor': 'top'
    },
    title_font_size=22,

    # Axes
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    xaxis={
        'tickangle': -45,
        'categoryorder': 'array',
        'categoryarray': categories,
        'showgrid': False
    },
    yaxis={
        'range': [0, 15],
        'dtick': 5,
        'showgrid': True,
        'gridcolor': '#E0E0E0'
    },
    
    # General Styling
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    
    # Margins to prevent clipping of titles or labels
    margin=dict(l=60, r=40, t=100, b=120)
)

# --- 5. Output the Image ---
# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the image file with a higher scale for better resolution
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")