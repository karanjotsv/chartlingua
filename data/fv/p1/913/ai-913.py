import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check if the JSON file path is provided
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Create a figure with two subplots for the pie charts
fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

# Extract data for both charts
data_export = chart_data['chart_data'][0]
data_import = chart_data['chart_data'][1]

# Add the first pie chart (Export)
fig.add_trace(go.Pie(
    labels=data_export['labels'],
    values=data_export['values'],
    marker_colors=data_export['colors'],
    pull=[0.05] * len(data_export['values']),
    textinfo='label',
    textposition='outside',
    sort=False,
    direction='clockwise',
    hoverinfo='label+percent',
    name=data_export['title']
), 1, 1)

# Add the second pie chart (Import)
fig.add_trace(go.Pie(
    labels=data_import['labels'],
    values=data_import['values'],
    marker_colors=data_import['colors'],
    pull=[0.05] * len(data_import['values']),
    textinfo='label',
    textposition='outside',
    sort=False,
    direction='clockwise',
    hoverinfo='label+percent',
    name=data_import['title']
), 1, 2)

# Update layout and add annotations
fig.update_layout(
    showlegend=False,
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    margin=dict(t=20, b=120, l=20, r=20),
    annotations=[
        go.layout.Annotation(
            text=f"<b>{data_export['title']}</b><br>{data_export['subtitle']}",
            align='center',
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.23,
            y=-0.1
        ),
        go.layout.Annotation(
            text=f"<b>{data_import['title']}</b><br>{data_import['subtitle']}",
            align='center',
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.77,
            y=-0.1
        )
    ],
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Set common properties for the pie traces
fig.update_traces(
    outsidetextfont=dict(size=14, color='black'),
    insidetextorientation='radial'
)

# Determine output filename from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")