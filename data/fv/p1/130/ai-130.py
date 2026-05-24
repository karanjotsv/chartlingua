import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data_json = json.load(f)

# Extract data for the charts
chart_data = chart_data_json['chart_data']

# Create subplots for the two pie charts
fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

# Add the first pie chart
pie1_data = chart_data[0]
fig.add_trace(go.Pie(
    labels=pie1_data['labels'],
    values=pie1_data['values'],
    text=pie1_data['text_labels'],
    textinfo='text',
    textposition=pie1_data['text_positions'],
    marker=dict(colors=pie1_data['colors'], line=dict(color='#000000', width=1)),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
), 1, 1)

# Add the second pie chart
pie2_data = chart_data[1]
fig.add_trace(go.Pie(
    labels=pie2_data['labels'],
    values=pie2_data['values'],
    text=pie2_data['text_labels'],
    textinfo='text',
    textposition=pie2_data['text_positions'],
    marker=dict(colors=pie2_data['colors'], line=dict(color='#000000', width=1)),
    hoverinfo='label+value',
    sort=False,
    direction='clockwise',
    insidetextorientation='radial'
), 1, 2)

# Update layout for a clean and accurate appearance
fig.update_layout(
    showlegend=False,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor='white',
    plot_bgcolor='white',
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

# Determine the output filename from the input JSON filename
filename_base = json_file_path.stem
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")