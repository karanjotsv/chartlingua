import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])

# Ensure the JSON file exists before proceeding.
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data and settings from the specified JSON file.
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for the pie chart trace.
labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
# Use text from data to ensure labels match the original chart, even if percentages don't sum to 100.
slice_texts = [f"{d['value']}%" for d in chart_data]

# Initialize the figure.
fig = go.Figure()

# Add the pie chart trace using data from the JSON file.
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=slice_texts,
    textinfo='text',
    hoverinfo='label+percent',
    marker=dict(
        colors=colors,
        line=dict(color='white', width=2.5)
    ),
    insidetextfont=dict(
        family="Arial",
        color='white',
        size=16
    ),
    sort=False,  # This is crucial to preserve the original order of slices.
    direction='clockwise'
))

# Configure the layout of the chart.
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center',
        font=dict(size=20)
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.05,
        xanchor="center",
        x=0.5,
        traceorder="normal"
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(t=80, b=120, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output filename from the input JSON filename.
output_filename = json_path.stem + ".png"

# Save the figure as a high-resolution PNG image.
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as '{output_filename}'")