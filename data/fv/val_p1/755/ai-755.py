import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the file path from command line arguments
json_file_path = Path(sys.argv[1])

# Check if the provided file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data from the file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = data['categories']
series = data['series']

# Initialize the figure
fig = go.Figure()

# Iterate through the series in the JSON and add them as traces to the figure
for i, s in enumerate(series):
    fig.add_trace(go.Scatter(
        x=categories,
        y=s['data'],
        name=s['name'],
        mode='lines',
        line=dict(color=colors[i], width=3),
        yaxis='y' if s['y_axis'] == 'y1' else 'y2'
    ))

# Update the layout of the figure
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        xanchor='center',
        font=dict(size=24)
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        tickmode='array',
        tickvals=[1994, 1996, 1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012],
        showline=True,
        linewidth=1,
        linecolor='black',
        gridcolor='#D3D3D3'
    ),
    yaxis=dict(
        title=texts['y1_axis_title'],
        side='left',
        range=[0, 140],
        tick0=0,
        dtick=20,
        showline=True,
        linewidth=1,
        linecolor='black',
        gridcolor='#D3D3D3'
    ),
    yaxis2=dict(
        title=texts['y2_axis_title'],
        overlaying='y',
        side='right',
        range=[0, 250000],
        tick0=0,
        dtick=50000,
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.35,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=80, r=80, t=100, b=120),
    autosize=False,
    width=800,
    height=600
)

# Determine the output image file path from the input JSON file path
output_file_path = json_file_path.with_suffix('.png')

# Save the figure as a high-resolution PNG image
fig.write_image(output_file_path, scale=2)

print(f"Chart successfully generated and saved to {output_file_path}")