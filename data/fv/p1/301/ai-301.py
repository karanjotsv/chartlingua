import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# This script is designed to be executed from the command line,
# with the path to the JSON data file provided as the sole argument.
# Example: python your_script_name.py your_data_file.json

if len(sys.argv) != 2:
    print("Usage: python <script.py> <path_to_json>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data and configuration from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data components from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly by extracting values from the list of dictionaries
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [item['text_label'] for item in chart_data]

# Create the pie chart trace. The original is a 3D chart, which is not a standard
# Plotly pie chart type. A 2D pie chart is created as the best-practice alternative.
# The 'Tibia' slice is pulled out to mimic the 'exploded' effect in the original image.
pie_trace = go.Pie(
    labels=labels,
    values=values,
    text=text_labels,
    textinfo='text',
    textposition='outside',
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    pull=[0, 0, 0.1, 0],
    rotation=90,
    direction='clockwise',
    sort=False,
    hoverinfo='label+percent'
)

# Initialize the figure
fig = go.Figure(data=[pie_trace])

# Update layout properties for a clean and accurate presentation
fig.update_layout(
    font=dict(family="Arial", size=12),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=True,
    legend=dict(
        x=1.05,
        y=0.5,
        xanchor='left',
        yanchor='middle'
    ),
    # Add margins to prevent labels or legend from being clipped
    margin=dict(l=100, r=180, t=40, b=40)
)

# Determine the output filename from the input JSON filename
output_filename = json_path.stem + ".png"
output_path = json_path.with_name(output_filename)

# Save the figure to a high-resolution PNG file
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")