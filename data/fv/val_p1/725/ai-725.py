import sys
import json
import plotly.graph_objects as go
import pathlib

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Load data from the JSON file specified in the command-line argument
json_file_path = sys.argv[1]
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and configuration from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for plotting
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the bar trace using data from the JSON
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    name=''  # Use an empty name to avoid a legend entry
))

# Construct the title string, combining title and subtitle if available
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Configure the layout of the chart
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
        'tickvals': x_values,
        'showgrid': False,
        'linecolor': 'black'
    },
    yaxis={
        'title_text': texts.get('y_axis_title'),
        'showgrid': True,
        'gridcolor': '#D3D3D3',
        'range': [0, 3500000000],
        'tickvals': list(range(0, 3500000001, 500000000))
    },
    plot_bgcolor='#EBEBEB',
    paper_bgcolor='white',
    font={'family': 'Arial', 'size': 12},
    showlegend=False,
    margin=dict(l=120, r=40, t=100, b=80) # Adjusted left margin for long y-axis labels
)

# Manually format y-axis tick labels to use dots as thousands separators
y_tick_vals = list(range(0, 3500000001, 500000000))
y_tick_text = [f"€ {val:,}".replace(",", ".") for val in y_tick_vals]
fig.update_yaxes(ticktext=y_tick_text, tickvals=y_tick_vals)

# Determine the output filename from the input JSON file path
output_path = pathlib.Path(json_file_path)
output_filename = output_path.with_suffix('.png').name

# Save the figure to a PNG file with high resolution
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)