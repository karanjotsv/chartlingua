import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# Check if a file path is provided
if len(sys.argv) < 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
filename_base = json_file_path.stem

# --- 2. Create the Chart ---
# Initialize the figure
fig = go.Figure()

# Add traces (bars) to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None,
        # The original has no hover text, so we disable it
        hoverinfo='none'
    ))

# --- 3. Configure Layout and Styling ---
# Combine title and subtitle if available
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=80, b=80),  # Adjust margins for labels
    xaxis=dict(
        type='category',  # Treat x-axis labels as discrete categories
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside',
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        range=[0, 250],
        tickvals=[0, 50, 100, 150, 200, 250],
        showgrid=True,
        gridwidth=1,
        gridcolor='darkgrey',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside',
        tickfont=dict(size=14)
    )
)

# --- 4. Output the Image ---
# Define the output image filename
output_filename = f"{filename_base}.png"

# Write the image file with a higher resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")