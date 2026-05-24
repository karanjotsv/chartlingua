import sys
import json
import os
import plotly.graph_objects as go

# Check for required command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and settings from the JSON structure
chart_data = chart_spec.get('chart_data', [])
categories = chart_spec.get('categories', [])
texts = chart_spec.get('texts', {})
colors = chart_spec.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=categories,
        y=series.get('y', []),
        name=series.get('name', ''),
        mode='lines',
        line=dict(color=colors[i % len(colors)], width=2.5)
    ))

# Configure the layout of the chart
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        x=0.98,
        y=0.8,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(0,0,0,0)',  # Transparent background
        borderwidth=0
    ),
    margin=dict(l=50, r=50, t=30, b=50),
    title_text=texts.get('title')
)

# Configure the axes
fig.update_xaxes(
    title_text=texts.get('x_axis_title'),
    tickmode='array',
    tickvals=categories,
    showline=True,
    linewidth=1,
    linecolor='grey',
    showgrid=False,
    zeroline=False
)

fig.update_yaxes(
    title_text=texts.get('y_axis_title'),
    range=[0, 120],
    dtick=20,
    showline=False,
    showgrid=True,
    gridcolor='lightgrey',
    gridwidth=1,
    zeroline=True,
    zerolinecolor='grey',
    zerolinewidth=1
)

# Derive the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")