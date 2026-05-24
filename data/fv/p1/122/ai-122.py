import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])

# Ensure the JSON file exists before proceeding.
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Load data and configuration from the specified JSON file.
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for the pie chart trace.
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize the figure.
fig = go.Figure()

# Add the pie chart trace, ensuring data order is preserved.
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=1.5)
    ),
    hole=0,
    sort=False,
    direction='clockwise',
    textinfo='none',
    hoverinfo='label+percent',
    domain={'x': [0.2, 0.8], 'y': [0.55, 0.95]} # Position the pie in the upper central area
))

# Configure the layout of the chart.
fig.update_layout(
    title=dict(
        text=texts['title'],
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=22)
    ),
    legend=dict(
        orientation="v",
        y=0.65,
        yanchor="top",
        x=0.20,
        xanchor="left",
        traceorder='normal',
        itemsizing='constant',
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="#000000"
    ),
    margin=dict(l=40, r=40, t=100, b=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output filename from the input JSON filename.
output_filename = json_file_path.stem + ".png"

# Save the figure to a high-resolution PNG file.
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")