import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read the JSON data file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_file_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data and texts from the loaded JSON
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Create a new figure
fig = go.Figure()

# Add traces for each data series, preserving the order from the JSON
for i, series in enumerate(data_series):
    color = colors[i] if i < len(colors) else None
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode=series.get('mode', 'lines+markers'),
        line=dict(color=color),
        marker=dict(
            symbol=series.get('marker', {}).get('symbol'),
            color=color,
            size=8
        )
    ))

# Update the layout of the chart
fig.update_layout(
    title=dict(
        text=texts.get('title', ''),
        x=0.5,
        font=dict(size=16)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title', ''),
        showgrid=True,
        gridcolor='LightGray',
        range=[1900, 2250],
        tickmode='linear',
        dtick=50
    ),
    yaxis=dict(
        title=texts.get('y_axis_title', ''),
        showgrid=True,
        gridcolor='LightGray',
        range=[0, 30000000],
        tickmode='linear',
        dtick=5000000
    ),
    legend=dict(
        x=0.8,
        y=0.6,
        bgcolor='rgba(255,255,255,0.7)',
        bordercolor='Black',
        borderwidth=0
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    margin=dict(l=100, r=40, t=80, b=80),
    xaxis_linecolor='black',
    yaxis_linecolor='black'
)

# Determine the output filename from the input JSON path
base_name = Path(json_file_path).stem
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")