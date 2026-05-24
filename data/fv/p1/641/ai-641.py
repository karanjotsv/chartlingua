import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
# The original image is a 3D pie chart, which is a style not natively supported for data representation in Plotly.
# We will create a standard 2D pie chart that accurately represents the data.
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+percent',
    textinfo='percent',
    textfont_size=14,
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise',
    rotation=90 # Starts the first slice at the top
)])

# Update layout
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

source_text = texts.get('source', '')

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    margin=dict(t=80, b=100, l=40, r=40),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.20,
            xanchor='left',
            yanchor='bottom',
            align='left'
        )
    ] if source_text else []
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)