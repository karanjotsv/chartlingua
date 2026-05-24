import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
categories = data.get('categories', [])
series_data = data.get('series', [])

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        name=series.get('name'),
        x=series.get('values'),
        y=categories,
        orientation='h',
        marker_color=colors[i % len(colors)] if colors else None
    ))

# Build the title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Configure layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        font=dict(family="Arial", size=18)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridwidth=1,
        gridcolor='LightGray',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        autorange="reversed" # Ensures the first category in the list is at the top
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
        title_text=texts.get('legend_title')
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    # Adjust margins to prevent y-axis labels from being cut off
    margin=dict(l=280, r=30, t=80, b=80),
    height=600,
    width=800
)

# Determine the output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")