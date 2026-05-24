import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data, texts, and colors from the JSON structure
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly
labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    texttemplate='%{label}<br>%{value}%',
    textposition='inside',
    textfont=dict(color='white', size=16),
    sort=False,  # Preserve the original order from the JSON data
    direction='clockwise',
    hole=0
))

# Update the layout of the figure
fig.update_layout(
    showlegend=False,
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(family="Arial", color="white"),
    margin=dict(l=20, r=20, t=20, b=20),
    autosize=False,
    width=800,
    height=800,
)

# Build the title string if a title or subtitle is present
title_text = ""
if texts.get('title'):
    title_text += texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

if title_text:
    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            xanchor='center'
        )
    )

# Define the output image path from the input JSON file name
output_image_path = json_file_path.with_suffix(".png")

# Save the figure as a high-resolution PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to '{output_image_path}'")