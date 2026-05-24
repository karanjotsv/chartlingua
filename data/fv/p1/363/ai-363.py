import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for plotting
data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Create a Plotly figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color=colors[i], width=2)
    ))

# Build title and source strings
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout to match the original chart
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=20)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=data_series[0]['x'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[-14000, 4000],
        tickvals=[-14000, -12000, -10000, -8000, -6000, -4000, -2000, 0, 2000, 4000],
        showgrid=True,
        gridcolor='LightGray',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='Gray',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation='v',
        yanchor="top",
        y=0.7,
        xanchor="right",
        x=0.98
    ),
    margin=dict(l=80, r=40, t=80, b=50)
)

# Generate the output filename from the input JSON path
output_filename = json_file_path.stem + '.png'

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")