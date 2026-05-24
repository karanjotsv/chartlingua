import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
categories = chart_data.get('categories', [])
series_data = chart_data.get('series', [])

# Create a new figure
fig = go.Figure()

# Add a bar trace for each series, preserving the order from the JSON
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('data', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)]
    ))

# Update the layout of the chart
fig.update_layout(
    barmode='group',
    title={
        'text': texts.get('title'),
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 18
        }
    },
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        linecolor='black'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False,
        range=[60, 95],
        linecolor='black'
    ),
    legend=dict(
        x=1.02,
        y=1,
        xanchor='left',
        yanchor='top'
    ),
    margin=dict(l=80, r=200, t=80, b=80)
)

# Determine the output filename from the input JSON filename
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")