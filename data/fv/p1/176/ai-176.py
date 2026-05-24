import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = Path(sys.argv[1])

# Read data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract data for the chart
chart_data = data.get('chart_data', [])
texts = data.get('texts', {})
colors = data.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
pie_texts = texts.get('pie_labels', [])

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    text=pie_texts,
    textinfo='text',
    textposition='inside',
    textfont=dict(
        family="Arial",
        size=16,
        color='white'
    ),
    marker=dict(
        colors=colors,
        line=dict(color='black', width=3)
    ),
    hoverinfo='label+percent',
    pull=[0.1, 0, 0, 0],
    sort=False,
    direction='clockwise'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout
fig.update_layout(
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(
        family="Arial",
        color="white"
    ),
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20)
)

# Define the output image file path
output_filename = json_path.stem + '.png'

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")