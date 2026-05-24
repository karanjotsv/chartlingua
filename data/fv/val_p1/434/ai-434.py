import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])

# Verify that the specified JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Load the chart data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded configuration
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for the Plotly pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure and add the pie chart trace
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,  # Preserve the order of slices as defined in the JSON data
    direction='clockwise'
))

# Construct the title string, including a subtitle if present
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the layout of the chart
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=True,
    legend=dict(
        traceorder='normal'  # Ensure legend order matches data order
    ),
    margin=dict(t=80, b=50, l=50, r=50),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Define the output image file path based on the input JSON file name
output_image_path = json_file_path.with_suffix('.png')

# Save the chart to a PNG file with a high resolution
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")