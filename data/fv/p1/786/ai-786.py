import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for the chart
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    texttemplate='%{label},<br>%{value}%',
    textposition='inside',
    insidetextfont=dict(family="Arial", size=16, color='black'),
    hoverinfo='label+percent',
    pull=[0.1] * len(labels),  # Explode all slices slightly to mimic the original
    sort=False, # Preserve the order from the JSON file
    direction='clockwise'
))

# Update layout
fig.update_layout(
    title_text=texts.get('title', ''),
    title_x=0.5,
    title_font=dict(family="Arial", size=24, color='black'),
    font=dict(family="Arial", size=12, color='black'),
    showlegend=False,
    margin=dict(t=100, b=50, l=50, r=50) # Adjust margins to prevent clipping
)

# Define output filename based on the input JSON filename
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have the 'kaleido' package installed (`pip install kaleido`)")
    sys.exit(1)