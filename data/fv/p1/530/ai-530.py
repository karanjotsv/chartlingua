import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)]
    ))

# Combine title and subtitle using HTML for better layout control
title_text = f"{texts['title']}<br><sup>{texts['subtitle']}</sup>" if texts['subtitle'] else texts['title']

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.98,
        x=0.05,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        range=[4, 89],
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 51],
        dtick=5,
        showgrid=True,
        gridcolor='lightgray'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=50, r=20, t=140, b=50),
    bargap=0.15
)

# Determine the output filename from the input JSON filename
output_filename = json_file_path.stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")