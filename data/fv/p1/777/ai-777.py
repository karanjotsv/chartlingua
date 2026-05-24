import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python script.name.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    showlegend=False
))

# Update layout
fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(
        family="Arial",
        size=16
    ),
    plot_bgcolor='white',
    xaxis=dict(
        type='category',
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='grey',
        gridwidth=1,
        zeroline=False,
        range=[0, 1.2],
        dtick=0.2,
        linecolor='black'
    ),
    margin=dict(l=80, r=40, t=80, b=80),
    showlegend=False
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")