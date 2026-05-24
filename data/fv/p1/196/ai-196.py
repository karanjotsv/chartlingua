import sys
import json
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_json.get('chart_data', [])
texts = chart_json.get('texts', {})
colors = chart_json.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    showlegend=False
))

# Build the title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout
fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis={
        'title_text': texts.get('x_axis_title'),
        'tickangle': -90,
        'showgrid': False
    },
    yaxis={
        'title_text': texts.get('y_axis_title'),
        'range': [0, 50],
        'tickvals': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        'gridcolor': 'lightgrey'
    },
    font={
        'family': "Arial",
        'size': 12
    },
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=80, b=120),  # Increased bottom margin for rotated labels
    showlegend=False
)

# Determine the output filename from the input JSON path
base_name = json_path.rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

# Save the figure to a file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")