import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])
filename_base = json_file_path.stem

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for Plotly horizontal bar chart
# Data must be reversed for Plotly to display it in the original top-to-bottom order
categories = [d['category'] for d in chart_data][::-1]
values = [d['value'] for d in chart_data][::-1]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker_color=colors[0] if colors else 'blue',
    showlegend=False
))

# Update layout to match the original image
fig.update_layout(
    title=dict(
        text=texts.get("title", ""),
        x=0.05,
        xanchor='left',
        font=dict(size=24)
    ),
    xaxis=dict(
        title=texts.get("x_axis_title", ""),
        range=[0, 70],
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False
    ),
    yaxis=dict(
        title=texts.get("y_axis_title", ""),
        showgrid=False,
        zeroline=False
    ),
    font=dict(
        family="Arial",
        size=16
    ),
    plot_bgcolor='white',
    paper_bgcolor='#F5F8F5',
    margin=dict(l=180, r=40, t=100, b=80),
    height=600,
    width=800
)

# Save the figure as a PNG image
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")