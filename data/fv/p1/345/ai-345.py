import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
base_filename = Path(json_file_path).stem

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and text from the loaded JSON
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=[d['x'] for d in data],
    y=[d['y'] for d in data],
    marker_color=colors[0] if colors else None,
    name='' # Use an empty name to avoid a legend item
))

# Update layout
fig.update_layout(
    title_text=texts.get('title', ''),
    title_x=0.5,
    xaxis_title=texts.get('x_axis_title', ''),
    yaxis_title=texts.get('y_axis_title', ''),
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        type='category',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        range=[0, 3.5],
        tickmode='linear',
        dtick=0.5,
        gridcolor='#cccccc',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=80, b=80)
)

# Define output filename and save the image
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")