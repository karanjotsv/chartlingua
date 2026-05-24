import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the chart data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Create a new figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(color=colors[i], width=3),
        connectgaps=False # Ensures gaps for null values
    ))

# Update the layout of the figure
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        font=dict(size=18)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=[1971, 1973, 1975, 1977, 1979, 1981, 1983, 1985, 1987],
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 160000],
        tickmode='array',
        tickvals=[0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000],
        gridcolor='#C8C8C8',
        gridwidth=1,
        zeroline=False
    ),
    plot_bgcolor='#EAE3D4',
    paper_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=60, r=40, t=80, b=100)
)

# Determine the output filename from the input JSON path
filename_base = Path(json_path).stem
output_filename = f"{filename_base}.png"

# Save the figure to a PNG image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")