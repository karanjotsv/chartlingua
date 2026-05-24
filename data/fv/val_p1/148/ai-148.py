import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data from the JSON object
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
shapes = chart_info.get("shapes", [])

# Initialize the figure
fig = go.Figure()

# Add data series to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series["x"],
        y=series["y"],
        mode='lines',
        name=series.get("name", ""),
        line=dict(color=colors[i % len(colors)], width=2, shape='spline'),
        showlegend=False
    ))

# Prepare layout object
layout = {
    "font": dict(family="Arial", size=14, color="black"),
    "plot_bgcolor": "white",
    "paper_bgcolor": "white",
    "showlegend": False,
    "margin": dict(l=60, r=40, t=40, b=60),
    "xaxis": {
        "title_text": texts.get("x_axis_title"),
        "range": [0, 90],
        "tickmode": 'linear',
        "dtick": 10,
        "showline": True,
        "linewidth": 1,
        "linecolor": 'black',
        "mirror": True,
        "ticks": 'outside',
        "gridcolor": 'lightgray',
        "zeroline": False
    },
    "yaxis": {
        "title_text": texts.get("y_axis_title"),
        "range": [0, 5],
        "tickmode": 'linear',
        "dtick": 1,
        "showline": True,
        "linewidth": 1,
        "linecolor": 'black',
        "mirror": True,
        "ticks": 'outside',
        "gridcolor": 'lightgray',
        "zeroline": False
    }
}

# Add annotations if they exist
if "annotations" in texts and texts["annotations"]:
    layout["annotations"] = texts["annotations"]
    for ann in layout["annotations"]:
        if 'font' not in ann:
            ann['font'] = {}
        ann['font']['family'] = "Arial"
        ann['font']['color'] = "black"

# Add shapes if they exist
if shapes:
    layout["shapes"] = shapes

# Apply the layout to the figure
fig.update_layout(layout)

# Define the output filename
output_filename = json_file_path.with_suffix('.png')

# Write the image to a file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")