import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Ensure a single command-line argument is provided for the JSON file path
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Validate and read the JSON file
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (json.JSONDecodeError, UnicodeDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Initialize the figure
fig = go.Figure()

# Iterate through the data series in the JSON and add them as traces
for i, series in enumerate(chart_data):
    series_color = colors[i % len(colors)] if colors else '#1f77b4'
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        mode='lines+markers',
        name=series.get("name", ""),
        line=dict(color=series_color),
        marker=dict(
            color=series_color,
            symbol='diamond',
            size=8
        )
    ))

# Apply layout, styling, and text from the JSON
fig.update_layout(
    title=dict(
        text=texts.get("title", ""),
        x=0.5,
        y=0.95,
        xanchor='center',
        font=dict(size=16)
    ),
    xaxis=dict(
        title=texts.get("x_axis_title", ""),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=False,
        tickmode='array',
        tickvals=chart_data[0].get('x', []) if chart_data else None
    ),
    yaxis=dict(
        title=texts.get("y_axis_title", ""),
        showgrid=True,
        gridcolor='#FFFFFF',
        gridwidth=1,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=False,
        zeroline=False,
        range=[0, 350]
    ),
    plot_bgcolor='#D3D3D3',
    paper_bgcolor='#FFFFFF',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=80, b=80)
)

# Define the output filename based on the input JSON filename
output_filename = json_path.stem + ".png"

# Write the figure to a high-resolution PNG image file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)