import sys
import json
import plotly.graph_objects as go
import pathlib

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Load data and settings from the specified JSON file.
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly by extracting labels and values.
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure.
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=1)
    ),
    textinfo='none',
    hoverinfo='label+percent',
    sort=False  # Preserve the order from the JSON file.
)])

# Update the layout for a clean, professional appearance.
fig.update_layout(
    title=texts.get('title'),
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(
        family="Arial",
        color='white'
    ),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    margin=dict(t=30, b=60, l=30, r=30)
)

# Determine the output image filename from the input JSON filename.
output_filename_base = json_file_path.stem
output_image_path = f"{output_filename_base}.png"

# Save the generated chart to a high-resolution PNG file.
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")