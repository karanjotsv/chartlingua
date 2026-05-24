import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_filepath = Path(sys.argv[1])

# Check if the provided path is a valid file
if not json_filepath.is_file():
    print(f"Error: File not found at {json_filepath}")
    sys.exit(1)

# Define the output image filename based on the input JSON filename
output_filename = json_filepath.with_suffix(".png")

# Read and load the JSON data from the file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_filepath}")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_spec.get('chart_data', [])
texts = chart_spec.get('texts', {})
colors = chart_spec.get('colors', [])

# Prepare the data series for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=3)
    ),
    texttemplate='%{value}%',
    textposition='inside',
    textfont=dict(
        family="Arial",
        size=16,
        color='white'
    ),
    hoverinfo='label+percent',
    sort=False,  # This is critical to preserve the original data order
    direction='clockwise'
))

# Update the layout for title, legend, fonts, and margins
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=24)
    ),
    legend=dict(
        traceorder='normal',
        orientation='v',
        yanchor='top',
        y=0.8,
        xanchor='left',
        x=0.85, # Position legend to the right of the pie
        font=dict(family="Arial", size=12)
    ),
    font=dict(family="Arial", size=12),
    margin=dict(l=40, r=420, t=100, b=40), # Ensure enough right margin for long legend labels
    paper_bgcolor='white',
    plot_bgcolor='white',
    width=800,
    height=500
)

# Write the generated chart to a PNG file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)