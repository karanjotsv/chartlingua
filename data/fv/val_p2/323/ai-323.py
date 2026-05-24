import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", {})

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors.get("bar_fill", "#9999FF"),
    marker_line_color=colors.get("bar_border", "#00008B"),
    marker_line_width=1.5,
    showlegend=False
))

# Update layout to match the original chart's style
fig.update_layout(
    title_text=texts.get("title"),
    title_x=0.5,
    xaxis_title=texts.get("x_axis_title"),
    yaxis_title=texts.get("y_axis_title"),
    font_family="Arial",
    font_size=12,
    xaxis=dict(
        tickangle=-45,
        showgrid=False
    ),
    yaxis=dict(
        range=[0, 80],
        dtick=10,
        showgrid=True,
        gridcolor=colors.get("grid", "#B0B0B0"),
        gridwidth=1
    ),
    plot_bgcolor=colors.get("plot_bg", "#DCDCDC"),
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=80, b=120),  # Adjust margins for labels
    showlegend=False
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")