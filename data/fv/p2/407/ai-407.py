import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read the JSON data file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Create the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(data_series):
    color = colors[i % len(colors)] if colors else '#1f77b4'
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines+markers',
        name=series.get('name', ''),
        line=dict(color=color, width=2),
        marker=dict(color=color, size=8, symbol='circle'),
        showlegend=False
    ))

# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text = f"<b>{title_text}</b><br>{texts.get('subtitle')}"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.85,
        xanchor='center',
        y=0.95,
        yanchor='top'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=100, b=80),
    xaxis=dict(
        showline=True,
        linewidth=2,
        linecolor='black',
        ticks='outside',
        tickwidth=1,
        tickcolor='black',
        gridcolor='white',
        zeroline=False
    ),
    yaxis=dict(
        showline=True,
        linewidth=2,
        linecolor='black',
        ticks='outside',
        tickwidth=1,
        tickcolor='black',
        gridcolor='white',
        zeroline=False,
        range=[0, 55]
    ),
    showlegend=False
)

# Derive output filename from JSON path
output_filename_base = pathlib.Path(json_path).stem
output_png_path = f"{output_filename_base}.png"

# Write image to file
fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")