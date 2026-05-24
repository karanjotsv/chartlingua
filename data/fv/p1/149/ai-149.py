import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON data file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
data = chart_data.get("chart_data", [])
texts = chart_data.get("texts", {})
colors = chart_data.get("colors", [])
bg_color = chart_data.get("background_color", "white")

# Prepare data for the pie chart
labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=0.5)),
    hoverinfo='label+percent',
    textinfo='percent',
    textposition='outside',
    textfont=dict(family="Arial", size=14, color='black'),
    sort=False,
    direction='clockwise',
    rotation=-6  # Adjusts the start angle to match the source image
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Build the title string from JSON data
title_text = texts.get('title', '')

# Update the layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    title_font=dict(
        family="Arial",
        size=22,
        color='black'
    ),
    font=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    paper_bgcolor=bg_color,
    plot_bgcolor=bg_color,
    margin=dict(l=50, r=50, t=100, b=100) # Adjust margins for labels and legend
)

# Determine the output filename from the input JSON path
filename_base = os.path.basename(json_path).replace('.json', '')
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")