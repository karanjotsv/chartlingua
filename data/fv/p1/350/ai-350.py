import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

# Create figure
fig = go.Figure()

# Add traces
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('name', ''),
        line=dict(color=colors[i % len(colors)], width=2.5),
        showlegend=False
    ))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    margin=dict(l=80, r=40, t=20, b=100),
    xaxis=dict(
        range=[54, 96],
        showline=True,
        linewidth=1.5,
        linecolor='#002D62',
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        title_text=""
    ),
    yaxis=dict(
        range=[-0.05, 1.05],
        title=dict(
            text=texts.get('y_axis_title'),
            font=dict(size=16)
        ),
        showline=True,
        linewidth=1.5,
        linecolor='#002D62',
        showticklabels=False,
        showgrid=False,
        zeroline=False
    ),
    annotations=texts.get('custom_annotations', [])
)

# Generate output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)