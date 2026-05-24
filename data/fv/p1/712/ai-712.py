import sys
import json
import os
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read the chart data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data for plotting
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
paper_bgcolor = config.get('paper_bgcolor', '#FFFFFF')

# Create the pie chart trace
pie_trace = go.Pie(
    labels=[d['label'] for d in chart_data],
    values=[d['value'] for d in chart_data],
    marker=dict(colors=colors, line=dict(color='#000000', width=0)),
    hoverinfo='label+percent',
    textinfo='percent',
    textfont=dict(family="Arial", size=12, color='black'),
    textposition='outside',
    sort=False,  # Preserve the original data order
    direction='clockwise',
    rotation=-30 # Adjusts the starting angle to match the source image
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Format the title by combining title and subtitle
title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

# Update the layout of the figure
fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,  # Position legend below the chart
        xanchor="center",
        x=0.5
    ),
    paper_bgcolor=paper_bgcolor,
    plot_bgcolor=paper_bgcolor,
    margin=dict(l=50, r=50, t=100, b=120)  # Adjust margins for title and legend
)

# Determine the base filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image with a higher resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")