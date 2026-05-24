import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Load data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Prepare data for Plotly
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
    marker_color=colors[0] if colors else '#FF0000',
    name=''
))

# Update layout
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title=texts.get('x_axis_title', ''),
    yaxis_title=texts.get('y_axis_title', ''),
    font={'family': "Arial", 'size': 14},
    plot_bgcolor='white',
    showlegend=False,
    xaxis={
        'type': 'category',
        'showline': True,
        'linewidth': 1,
        'linecolor': 'black',
        'ticks': 'outside',
        'tickfont': {'size': 14}
    },
    yaxis={
        'range': [0, 1.5],
        'tickvals': [0, 0.5, 1.0, 1.5],
        'showline': True,
        'linewidth': 1,
        'linecolor': 'black',
        'showgrid': True,
        'gridcolor': 'darkgrey',
        'tickfont': {'size': 14}
    },
    margin={'l': 80, 'r': 40, 't': 80, 'b': 80}
)

# Define output filename
output_filename = json_file_path.with_suffix('.png')

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")