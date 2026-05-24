import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data and configuration from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_file_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(data_series):
    color = colors[i % len(colors)] if colors else None
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(
            color=color,
            width=2,
            dash=series.get('line_style', 'solid')
        )
    ))

# Update layout and styling
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=14
    ),
    xaxis=dict(
        range=[0, 1000],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=False
    ),
    yaxis=dict(
        range=[0, 140],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=60, r=40, t=80, b=80)
)

# Determine the output filename from the input JSON path
input_path = Path(json_file_path)
output_filename = input_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")