import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_file_path}' contains invalid JSON.")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])
layout_options = config.get('layout_options', {})

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    textinfo='percent',
    hoverinfo='label+percent',
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise',
    textfont=dict(family="Arial", size=14, color='black'),
    marker=dict(line=dict(color='white', width=1)) # Add a subtle line between slices
))

# Update layout properties
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center',
        font=dict(family="Arial", size=22)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5,
        font=dict(family="Arial", size=12)
    ),
    font=dict(
        family="Arial"
    ),
    paper_bgcolor=layout_options.get('paper_bgcolor'),
    plot_bgcolor=layout_options.get('plot_bgcolor'),
    margin=dict(l=40, r=40, t=100, b=100) # Adjust margins to prevent clipping
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the chart to a high-resolution PNG file
fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to '{output_image_path}'")