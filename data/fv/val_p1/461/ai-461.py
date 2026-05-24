import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read JSON data from the file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Create figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(color=colors[i] if i < len(colors) else None, width=2)
    ))

# Build title and source strings using HTML for formatting
title_text = ''
if texts.get('title'):
    title_text += texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(text=title_text, x=0.5),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    width=835,
    height=626,
    margin=dict(l=60, r=20, t=40, b=80),
    xaxis=dict(
        range=[15, 65.5],
        dtick=5,
        showgrid=True,
        gridcolor='black',
        gridwidth=0.5,
        minor=dict(
            dtick=1,
            showgrid=True,
            gridcolor='lightgrey',
            gridwidth=0.25
        ),
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),
    yaxis=dict(
        range=[15, 65.5],
        dtick=5,
        showgrid=True,
        gridcolor='black',
        gridwidth=0.5,
        minor=dict(
            dtick=1,
            showgrid=True,
            gridcolor='lightgrey',
            gridwidth=0.25
        ),
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
        bordercolor="black",
        borderwidth=1
    )
)

# Determine output filename
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")