import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data from the loaded JSON
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
shapes = chart_info.get("shapes", [])
annotations = chart_info.get("annotations", [])

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        name=series.get("name"),
        mode='lines',
        line=dict(color=colors[i] if i < len(colors) else None, width=2)
    ))

# Update layout with titles, axis labels, and other styling
fig.update_layout(
    font=dict(family="Arial", size=12),
    title=texts.get("title"),
    xaxis_title=texts.get("x_axis_title"),
    yaxis_title=texts.get("y_axis_title"),
    yaxis_type="log",
    yaxis=dict(
        showgrid=True,
        gridcolor='#CCCCCC',
        gridwidth=1,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        exponentformat='power',
        tickfont=dict(size=12)
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=80, r=40, t=50, b=80),
    shapes=shapes,
    annotations=annotations
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")