import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read and parse the JSON data from the file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data and settings from the JSON object
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors),
    texttemplate='%{value:.1f}%',
    textposition='outside',
    sort=False,  # This is crucial to preserve the order from the JSON data
    direction='counterclockwise',
    rotation=91 # Start angle to position the smallest slices at the top
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Apply layout settings
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f'<br><span style="font-size:0.8em;color:grey;">{texts["subtitle"]}</span>'

fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.5,
    font_family="Arial",
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=40, r=40, t=40, b=120), # Increased bottom margin for legend
    paper_bgcolor='white'
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to '{output_image_path}'")