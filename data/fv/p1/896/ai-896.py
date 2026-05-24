import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data from the JSON structure
chart_data = chart_config.get('chart_data', [])
colors = chart_config.get('colors', [])
texts = chart_config.get('texts', {})

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
slice_texts = [item.get('text', '') for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    text=slice_texts,
    textinfo='text',
    marker_colors=colors,
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    textposition='inside',
    insidetextorientation='horizontal'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout for a clean appearance matching the original
fig.update_layout(
    showlegend=False,
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(
        family="Arial",
        size=18,
        color="white"
    ),
    margin=dict(t=20, b=20, l=20, r=20),
    uniformtext_minsize=12,
    uniformtext_mode='hide'
)

# Update trace-specific properties
fig.update_traces(
    hoverinfo='label+percent',
    textfont_size=20
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)