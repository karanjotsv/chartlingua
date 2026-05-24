import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Create the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series['category'],
        x=[series['category']],  # Each bar is its own category on the x-axis
        y=[series['value']],
        marker_color=colors[i],
        text=[f"{series['value']}"],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=16,
            color=series['text_color']
        ),
        error_y=dict(
            type='data',
            array=[series['error']],
            visible=True,
            color='dimgrey',
            thickness=1.5
        ),
        showlegend=True,
        width=0.7 # Control bar width
    ))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        title_font=dict(size=14),
        showticklabels=False,
        zeroline=False,
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_font=dict(size=14),
        range=[-250, 650],
        tickvals=[-200, 0, 200, 400, 600],
        gridcolor='#E5E5E5',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
        font=dict(size=14),
        traceorder="normal"
    ),
    margin=dict(l=60, r=30, t=80, b=80),
    bargap=0.6 # Increase gap between bars of different categories
)

# Define output filename based on the input JSON filename
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")