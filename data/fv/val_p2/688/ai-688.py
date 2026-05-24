import sys
import json
import plotly.graph_objects as go
import os

# Check for the required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data and configuration from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in file '{json_file_path}'")
    sys.exit(1)

# Extract data for the chart
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    sort=False,
    direction='clockwise',
    rotation=108,  # Adjust rotation to match the original image's slice orientation
    textinfo='none', # Hide default percentage labels
    hoverinfo='label+percent'
))

# Update layout for a clean and accurate appearance
fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    title_y=0.95,
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.7,
        xanchor="right",
        x=0.98,
        traceorder='normal',
        bgcolor='rgba(255,255,255,0)' # Transparent background for the legend
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=40, r=40, t=80, b=40)
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)