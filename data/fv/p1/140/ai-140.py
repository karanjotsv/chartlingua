import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)


# Prepare data for Plotly
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# The original image doesn't sum the sub-pie to the parent slice value.
# To replicate a "pie of pie" visually, we need a slice to expand.
# We will represent the 4% "Baryonic Matter" as the sum of its components for the sub-pie.
# The labels in the chart, however, will be preserved from the JSON.
main_labels = data['main_pie']['labels']
main_values = data['main_pie']['values']
sub_labels = data['sub_pie']['labels']
sub_values = data['sub_pie']['values']

# Assign colors. The sub-pie values are represented with more colors than the chart shows.
# We will assign them in order.
main_colors = colors[:len(main_labels)]
sub_colors = colors[len(main_labels):]

# Create the figure
fig = go.Figure()

# Add the main pie chart trace
fig.add_trace(go.Pie(
    labels=main_labels,
    values=main_values,
    domain={'x': [0, 0.48], 'y': [0.1, 0.9]},
    marker={'colors': main_colors, 'line': {'color': 'black', 'width': 1.5}},
    textinfo='percent',
    textfont={'family': 'Arial', 'size': 16, 'color': 'black'},
    hoverinfo='label+percent',
    name='Main Composition',
    sort=False,
    direction='clockwise',
    rotation=115
))

# Add the sub pie chart trace
fig.add_trace(go.Pie(
    labels=sub_labels,
    values=sub_values,
    domain={'x': [0.52, 1.0], 'y': [0, 1]},
    marker={'colors': sub_colors, 'line': {'color': 'black', 'width': 1.5}},
    textinfo='percent',
    textfont={'family': 'Arial', 'size': 16, 'color': 'black'},
    hoverinfo='label+percent',
    name='Baryonic Matter Details',
    sort=False
))

# Update layout
fig.update_layout(
    showlegend=True,
    paper_bgcolor='black',
    plot_bgcolor='rgba(0,0,0,0)',
    font={'family': 'Arial', 'color': 'white', 'size': 14},
    legend={'traceorder': 'normal'},
    margin={'t': 60, 'b': 20, 'l': 20, 'r': 20},
    width=1000,
    height=500
)

# Add shapes to connect the pies
# Coordinates are in 'paper' reference (from 0 to 1 for the whole plot)
fig.add_shape(type="line",
    xref="paper", yref="paper",
    x0=0.46, y0=0.6, x1=0.52, y1=0.85,
    line=dict(color="black", width=1.5)
)
fig.add_shape(type="line",
    xref="paper", yref="paper",
    x0=0.45, y0=0.47, x1=0.52, y1=0.15,
    line=dict(color="black", width=1.5)
)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)