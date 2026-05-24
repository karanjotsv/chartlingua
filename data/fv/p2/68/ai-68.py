import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly trace
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create a new figure
fig = go.Figure()

# Add the bar chart trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    marker_line_color='black',
    marker_line_width=1.5,
    showlegend=False
))

# Configure the layout to match the original chart
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=20, t=40, b=250),  # Increased bottom margin for rotated labels
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        type='log',
        range=[-1, 3],  # Logarithmic range for 0.1 to 1000
        tickvals=[0.1, 1, 10, 100, 1000],
        ticktext=['0.1', '1', '10', '100', '1000'],
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        zeroline=False
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickangle=-90,
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    )
)

# Derive the output filename from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Write the figure to a PNG file with high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")