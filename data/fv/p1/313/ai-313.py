import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])

# Ensure the specified JSON file exists before proceeding.
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Load all chart data and text from the specified JSON file.
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data structures for Plotly from the loaded JSON.
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure object.
fig = go.Figure()

# Add the pie chart trace.
# The `sort=False` argument is crucial to preserve the original data order from the JSON file.
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    sort=False,
    textinfo='none' # Hiding default percentage labels on slices
))

# Configure the layout of the chart.
# This includes setting the title, font, legend properties, and margins to prevent clipping.
fig.update_layout(
    title_text=texts.get('title', 'Default Title'),
    title_x=0.5,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,  # Position legend below the chart area
        xanchor="center",
        x=0.5,
        traceorder="normal"
    ),
    margin=dict(t=80, b=120, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Generate the output PNG file. The filename is derived from the input JSON filename.
# The scale factor is set to 2 for a higher-resolution image.
output_image_path = json_file_path.stem + '.png'
fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to '{output_image_path}'")