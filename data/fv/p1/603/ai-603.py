import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
# Ensure x-values are treated as categories by converting to strings
x_values = [str(item['x']) for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    name='' # No legend entry needed
))

# Update layout
fig.update_layout(
    title_text=texts.get('title', ''),
    title_x=0.5,
    xaxis_title_text=texts.get('x_axis_title', ''),
    yaxis_title_text=texts.get('y_axis_title', ''),
    font_family="Arial",
    font_size=16,
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=80, b=80),
    yaxis=dict(
        range=[0, 500],
        gridcolor='lightgray',
        gridwidth=1,
        zeroline=False
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False
    )
)

# Determine the output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)