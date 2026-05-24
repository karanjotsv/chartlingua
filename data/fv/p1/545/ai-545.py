import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from the JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', {})

# Create the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines+markers',
        line=dict(color=colors.get('series', [])[i]),
        marker=dict(
            color=colors.get('series', [])[i],
            symbol='square',
            size=8,
            line=dict(
                width=1,
                color=colors.get('axes_lines', '#000000')
            )
        )
    ))

# Build the title string
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts['subtitle']}"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=18)
    ),
    xaxis=dict(
        title=f"<b>{texts.get('x_axis_title', '')}</b>",
        tickvals=chart_data[0].get('x'),
        tickmode='array',
        showgrid=False,
        showline=True,
        linewidth=2,
        linecolor=colors.get('axes_lines', '#000000'),
        mirror=True
    ),
    yaxis=dict(
        title=f"<b>{texts.get('y_axis_title', '')}</b>",
        range=[0, 450],
        dtick=50,
        showgrid=True,
        gridcolor=colors.get('grid', '#CCCCCC'),
        gridwidth=1,
        showline=True,
        linewidth=2,
        linecolor=colors.get('axes_lines', '#000000'),
        mirror=True
    ),
    plot_bgcolor=colors.get('plot_bg', '#FFFFFF'),
    paper_bgcolor=colors.get('background', '#FFFFFF'),
    font=dict(
        family="Arial",
        color=colors.get('text', '#000000')
    ),
    legend=dict(
        x=0.98,
        y=0.8,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255,255,255,0.7)',
        bordercolor=colors.get('axes_lines', '#000000'),
        borderwidth=1
    ),
    margin=dict(l=80, r=40, t=80, b=80)
)

# Determine output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")