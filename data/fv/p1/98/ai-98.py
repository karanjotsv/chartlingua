import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]

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

# Extract data and texts from the loaded JSON
data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Create the figure
fig = go.Figure()

# Add a trace for each data point as a separate bar series
# This structure replicates the original chart's grouping under a single x-axis label.
for i, series in enumerate(data_series):
    fig.add_trace(go.Bar(
        x=['1'],  # Common x-axis category label from the original chart
        y=[series['value']],
        name=series['category'],
        marker_color=colors[i]
    ))

# Update layout
fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    yaxis_title_text=texts['y_axis_title'],
    xaxis_title_text=texts['x_axis_title'],
    font=dict(
        family="Arial",
        size=12
    ),
    barmode='group',
    plot_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    yaxis=dict(
        range=[0, 450],
        tickmode='linear',
        tick0=0,
        dtick=50,
        showgrid=True,
        gridcolor='lightgrey'
    ),
    xaxis=dict(
        showgrid=False,
        showline=False
    ),
    margin=dict(l=60, r=20, t=60, b=100) # Adjust margins for legend and titles
)

# Determine the output image filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")