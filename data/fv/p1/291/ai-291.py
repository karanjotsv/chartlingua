import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data and settings from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create a figure with two subplots for the pie charts
fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

# Add a pie chart trace for each data series
for i, chart in enumerate(chart_data):
    fig.add_trace(go.Pie(
        labels=chart['labels'],
        values=chart['values'],
        name=chart['title'],
        marker_colors=colors,
        pull=[0.05, 0.05, 0.05, 0.05],  # Slightly separate all slices
        sort=False,  # Preserve original data order
        textinfo='none',  # Hide default text on slices
        hoverinfo='label+percent'
    ), 1, i + 1)

# Update the layout of the figure
fig.update_layout(
    paper_bgcolor='#4A6B4A',
    plot_bgcolor='#4A6B4A',
    font=dict(family="Arial", color="black"),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5,
        font=dict(size=16)
    ),
    margin=dict(t=80, b=80, l=20, r=20),
    annotations=[
        dict(
            text=chart_data[0]['title'],
            x=0.22,
            y=1.05,
            xref="paper",
            yref="paper",
            font_size=28,
            showarrow=False
        ),
        dict(
            text=chart_data[1]['title'],
            x=0.78,
            y=1.05,
            xref="paper",
            yref="paper",
            font_size=28,
            showarrow=False
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")