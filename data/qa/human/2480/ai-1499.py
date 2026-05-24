import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided
if len(sys.argv) < 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data from the JSON object
data_series = chart_data['chart_data'][0]
# Reverse data for correct top-to-bottom display in Plotly horizontal bar charts
categories = data_series['categories'][::-1]
values = data_series['values'][::-1]
texts = chart_data['texts']
colors = chart_data['colors']

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{x:.2f}',
    cliponaxis=False  # Allow text to be drawn outside the plot area
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    title=None,
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='lightgrey',
        griddash='dot',
        zeroline=False
    ),
    yaxis=dict(
        showline=True,
        linewidth=1.5,
        linecolor='black'
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=40, t=50, b=80),
    # Add source annotation
    annotations=[
        dict(
            text=texts['source'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.15,
            xanchor='right',
            yanchor='top'
        )
    ]
)

# Define output filename based on the input JSON filename
output_filename = json_file_path.with_suffix('.png')

# Save the chart as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")