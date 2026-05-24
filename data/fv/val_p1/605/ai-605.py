import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_file_path}'")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

# Prepare data lists
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    name='' # No name needed for a single series with no legend
))

# Update layout
fig.update_layout(
    title_text=texts.get('title', ''),
    title_x=0.5,
    yaxis_title_text=texts.get('y_axis_title', ''),
    xaxis_title_text=texts.get('x_axis_title', ''),
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(t=80, b=100, l=60, r=20),
    xaxis=dict(
        tickangle=-45,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        range=[0, 20],
        dtick=5,
        showgrid=True,
        gridcolor='darkgrey',
        gridwidth=0.5,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside',
        minor=dict(
            ticks='outside',
            ticklen=5,
            showgrid=False
        )
    )
)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_image_filename, scale=2)
    print(f"Chart saved to {output_image_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)