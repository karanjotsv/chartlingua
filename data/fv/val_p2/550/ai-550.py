import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Derive the output filename from the JSON filename
output_filename_base = json_path.stem

# Read the JSON data
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data_json = json.load(f)

# Extract data and settings from the JSON
chart_data = chart_data_json.get("chart_data", [])
texts = chart_data_json.get("texts", {})
colors = chart_data_json.get("colors", [])
special_params = chart_data_json.get("special_params", {})

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(
            color=special_params.get("line_color", "#000000"),
            width=special_params.get("line_width", 1)
        )
    ),
    pull=special_params.get("pull", 0),
    rotation=special_params.get("rotation", 0),
    sort=False,  # Preserve the original data order
    direction='clockwise',
    hoverinfo='label+percent',
    textinfo='none'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout
fig.update_layout(
    title_text=texts.get('title') if texts.get('title') else None,
    font=dict(
        family="Arial",
        color=special_params.get("font_color", "#000000")
    ),
    showlegend=True,
    legend=dict(
        title_text=texts.get('legend_title') if texts.get('legend_title') else None,
        bgcolor='rgba(0,0,0,0)' # Transparent background for the legend
    ),
    paper_bgcolor=special_params.get("paper_bgcolor", "#FFFFFF"),
    plot_bgcolor=special_params.get("plot_bgcolor", "#FFFFFF"),
    margin=dict(l=40, r=40, t=80, b=40)
)

# Generate and save the image
output_path = f"{output_filename_base}.png"
fig.write_image(output_path, scale=2)

print(f"Chart saved as {output_path}")