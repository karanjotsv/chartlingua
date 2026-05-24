import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for required command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Read the JSON data
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly's multi-level x-axis and y-values
x_categories = [(item['category_level_1'], item['category_level_2']) for item in chart_data]
y_values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_categories,
    y=y_values,
    marker_color=colors[0],
    showlegend=False,
    width=0.7 # Adjust bar width for better visual separation
))

# Combine title and subtitle if available
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout to match the original image
fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 24}
    },
    font={
        'family': "Arial",
        'size': 12
    },
    xaxis={
        'title_text': texts.get('x_axis_title'),
        'tickmode': 'array',
        'showgrid': False,
        'linecolor': 'black',
        'ticks': '' # Hides tick marks but keeps labels
    },
    yaxis={
        'title_text': texts.get('y_axis_title'),
        'range': [0, 35],
        'dtick': 5,
        'showgrid': True,
        'gridcolor': 'lightgrey',
        'gridwidth': 1,
        'zeroline': False
    },
    plot_bgcolor='white',
    margin={'t': 80, 'b': 80, 'l': 50, 'r': 20},
    showlegend=False
)

# Add vertical lines to separate the main categories on the x-axis
fig.add_vline(x=1.5, line_width=1, line_color="black")

# Determine the output filename and save the image
output_filename = json_file_path.with_suffix('.png').name
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")