import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check if the path to the JSON file is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data_json = json.load(f)

# Extract data and texts from the JSON object
chart_data = chart_data_json.get("chart_data", [])
texts = chart_data_json.get("texts", {})
colors = chart_data_json.get("colors", [])

# Prepare data for Plotly
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
display_texts = [item['display_text'] for item in chart_data]

# Create the pie chart figure
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    text=display_texts,
    textinfo='text',
    textposition='outside',
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=2)
    ),
    hole=0,
    sort=False,
    direction='clockwise',
    hoverinfo='label+percent'
)])

# Update the layout of the figure
fig.update_layout(
    title=dict(
        text=texts.get("title"),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=80, r=80, t=120, b=40)
)

# Define the output image file path
output_image_path = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Image saved to {output_image_path}")