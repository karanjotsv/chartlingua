import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the file path from the command-line argument
json_path = Path(sys.argv[1])

# Check if the file exists
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read the JSON data from the file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for plotting
data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Create the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color=colors[i], width=2),
        showlegend=True
    ))

# Update layout
fig.update_layout(
    xaxis_type="log",
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 100],
        tickvals=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor='#D3D3D3',
        gridwidth=1,
        zeroline=False
    ),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=80, r=40, t=40, b=80)
)

# Define output filename
output_filename = json_path.with_suffix('.png').name

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")