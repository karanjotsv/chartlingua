import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data, texts, and colors from the JSON object
data_series = chart_data.get('chart_data', [])
chart_texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Create subplots
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.02,
    row_heights=[0.7, 0.3],
    subplot_titles=(chart_texts.get('title_1', ''), chart_texts.get('title_2', ''))
)

# Add traces to the subplots
if len(data_series) > 0:
    series1 = data_series[0]
    fig.add_trace(go.Scatter(
        x=series1['x'],
        y=series1['y'],
        mode='lines',
        name=series1['name'],
        line=dict(color=colors[0], width=1.5)
    ), row=1, col=1)

if len(data_series) > 1:
    series2 = data_series[1]
    fig.add_trace(go.Scatter(
        x=series2['x'],
        y=series2['y'],
        mode='lines',
        name=series2['name'],
        line=dict(color=colors[1], width=1.5)
    ), row=2, col=1)

# Update layout
fig.update_layout(
    height=600,
    width=800,
    showlegend=False,
    font=dict(family="Arial", size=12),
    margin=dict(l=50, r=20, t=50, b=40),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Align subplot titles to the left
fig.update_annotations(x=0, xanchor='left', font=dict(size=12))

# Update axes
fig.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='#d3d3d3',
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    ticks='outside',
    minor=dict(
        ticks="outside",
        ticklen=5,
        tickcolor="black",
        showgrid=True,
        gridcolor='#e9e9e9'
    ),
    tickformat='%Y'
)

# Update Y-axis for the top subplot
fig.update_yaxes(
    row=1, col=1,
    range=[100, 1700],
    dtick=200,
    showgrid=True,
    gridwidth=1,
    gridcolor='#d3d3d3',
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    ticks='outside',
    minor=dict(
        ticks="outside",
        ticklen=5,
        tickcolor="black",
        showgrid=True,
        gridcolor='#e9e9e9'
    )
)

# Update Y-axis for the bottom subplot
fig.update_yaxes(
    row=2, col=1,
    range=[-5, 105],
    dtick=20,
    showgrid=True,
    gridwidth=1,
    gridcolor='#d3d3d3',
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    ticks='outside'
)

# Set the x-axis range
fig.update_xaxes(range=[1994.8, 2009.8])


# Define the output image file path
output_image_path = json_file_path.with_suffix('.png')

# Write the image to a file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")