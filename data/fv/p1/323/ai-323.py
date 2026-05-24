import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the chart data and configuration from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_config.get("chart_data", [])
texts = chart_config.get("texts", {})
colors = chart_config.get("colors", [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    color_info = colors[i % len(colors)] if colors else {}
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        mode='lines+markers',
        name=series.get("name", ""),
        line=dict(color=color_info.get("line")),
        marker=dict(color=color_info.get("marker")),
    ))

# Update the layout of the figure
fig.update_layout(
    title=dict(
        text=texts.get("title"),
        x=0.5,
        font=dict(size=18)
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        range=[1, 10],
        tickmode='linear',
        tick0=1,
        dtick=1
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        type='log',
        range=[-3, 0], # Corresponds to 10^-3 to 10^0
        tickformat=".0e"
    ),
    font=dict(family="Arial", size=12),
    template="plotly_white",
    showlegend=False,
    margin=dict(t=80, b=80, l=80, r=40),
    autosize=False,
    width=800,
    height=600
)

# Define the output image file path
output_filename = json_file_path.with_suffix(".png")

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)