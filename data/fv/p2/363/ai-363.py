import sys
import json
import pathlib
import plotly.graph_objects as go

# This script requires a single command-line argument: the path to the JSON file.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
output_filename_base = pathlib.Path(json_path).stem

# Load data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

chart_data = chart_config.get('chart_data', {})
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series, iterating in order
categories = chart_data.get('categories', [])
series_list = chart_data.get('series', [])

for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('data', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)]
    ))

# Combine title and subtitle if they exist
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if title_text and subtitle_text:
    combined_title = f"{title_text}<br><sub>{subtitle_text}</sub>"
elif title_text:
    combined_title = title_text
else:
    combined_title = None

# Update layout for a professional appearance
fig.update_layout(
    barmode='group',
    title_text=combined_title,
    title_x=0.5,
    font_family="Arial",
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=False,
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 22],
        tick0=0,
        dtick=2,
        ticksuffix=texts.get('y_axis_suffix', ''),
        gridcolor='#cccccc',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=False,
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2, # Position legend below the x-axis
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=50, r=20, t=50, b=150) # Increased bottom margin for legend
)

# Output the chart as a PNG image file
output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")