import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data for the chart
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])
background_color = chart_data.get('background_color', '#FFFFFF')

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=0.5)),
    hole=0,
    sort=False,
    direction='clockwise',
    rotation=180,
    textinfo='percent',
    textposition='outside',
    textfont=dict(size=14, family="Arial", color='black'),
    hoverinfo='label+percent'
))

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center',
        y=0.95,
        yanchor='top',
        font=dict(family="Arial", size=24, color='black')
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
        font=dict(family="Arial", size=12)
    ),
    font=dict(family="Arial", size=12, color='black'),
    paper_bgcolor=background_color,
    plot_bgcolor=background_color,
    margin=dict(l=40, r=40, t=120, b=120)
)

# Determine output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)