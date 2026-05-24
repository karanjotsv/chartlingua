import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read the JSON data from the file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and settings from the JSON object
data_series = chart_data['chart_data']
color_series = chart_data['colors']

# Create a figure with two subplots for the pie charts
fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

# Add the first pie chart (main atmosphere composition)
pie1_data = data_series[0]
fig.add_trace(
    go.Pie(
        labels=pie1_data['labels'],
        values=pie1_data['values'],
        text=pie1_data['text_labels'],
        textinfo='none',
        texttemplate='%{text}',
        textposition='inside',
        marker_colors=color_series[0],
        sort=False,
        direction='clockwise',
        rotation=-13,
        domain=dict(x=[0.0, 0.48], y=[0.05, 0.95]),
        pull=[0, 0, 0.05]
    ),
    row=1, col=1
)

# Add the second pie chart (trace elements breakout)
pie2_data = data_series[1]
fig.add_trace(
    go.Pie(
        labels=pie2_data['labels'],
        values=pie2_data['values'],
        text=pie2_data['text_labels'],
        textinfo='none',
        texttemplate='%{text}',
        textposition='inside',
        marker_colors=color_series[1],
        sort=False,
        direction='clockwise',
        rotation=95,
        domain=dict(x=[0.52, 1.0], y=[0.0, 1.0])
    ),
    row=1, col=2
)

# Update layout for a clean, accurate appearance
fig.update_layout(
    showlegend=False,
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(family="Arial", color="black"),
    uniformtext_minsize=10,
    uniformtext_mode='hide',
    margin=dict(l=10, r=10, t=10, b=10),
    # Add shapes to create the breakout lines
    shapes=[
        # Top line
        go.layout.Shape(
            type="line",
            xref="paper", yref="paper",
            x0=0.47, y0=0.53, x1=0.52, y1=0.85,
            line=dict(color="#555555", width=1)
        ),
        # Bottom line
        go.layout.Shape(
            type="line",
            xref="paper", yref="paper",
            x0=0.47, y0=0.47, x1=0.52, y1=0.15,
            line=dict(color="#555555", width=1)
        )
    ]
)

# Determine the output filename from the input JSON path
json_path = pathlib.Path(json_file_path)
filename_base = json_path.stem
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2, width=800, height=400)

print(f"Chart saved to {output_filename}")