import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    sys.exit(1)

# Extract data from the JSON object
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', f'Series {i+1}'),
        mode='lines',
        line=dict(color=colors[i % len(colors)], width=2.5),
        showlegend=False
    ))

# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(text=title_text if title_text else None, x=0.05, xanchor='left'),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=30, t=40, b=50),
    xaxis=dict(
        tickmode='array',
        tickvals=[1990, 1992, 1994, 1996, 1998, 2000, 2002, 2004, 2006, 2008, 2010],
        showline=True,
        linewidth=1.5,
        linecolor='lightgrey',
        showgrid=False,
        ticks='outside',
        ticklen=5
    ),
    yaxis=dict(
        range=[0, 2400],
        tickmode='array',
        tickvals=[0, 600, 1200, 1800, 2400],
        showline=False,
        showgrid=True,
        gridcolor='lightgrey',
        gridwidth=1
    )
)

# Derive output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)