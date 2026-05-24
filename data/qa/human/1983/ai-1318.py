import sys
import json
import plotly.graph_objects as go
import os

# Check if the path to the JSON file is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_filepath = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_filepath):
    print(f"Error: JSON file not found at '{json_filepath}'")
    sys.exit(1)

# Read and parse the JSON file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_filepath}'")
    sys.exit(1)

# Extract data and text from the configuration
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for the pie chart
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=2)
    ),
    hoverinfo='label+percent',
    textinfo='label+percent',
    textposition='outside',
    sort=False,  # Preserve the original order from the JSON
    direction='clockwise',
    rotation=80 # Adjust rotation to match the original chart's starting point
))

# Update the layout for a clean and accurate appearance
fig.update_layout(
    showlegend=False,
    margin=dict(l=80, r=80, t=50, b=80),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('note', ''),
            x=0.0,
            y=-0.1,
            xref="paper",
            yref="paper",
            xanchor="left",
            yanchor="top",
            align="left"
        ),
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            x=1.0,
            y=-0.1,
            xref="paper",
            yref="paper",
            xanchor="right",
            yanchor="top",
            align="right"
        )
    ]
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_filepath))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as '{output_filename}'")