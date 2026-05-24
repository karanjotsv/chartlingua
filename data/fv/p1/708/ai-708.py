import sys
import json
import plotly.graph_objects as go
import pathlib

# This script requires a single command-line argument: the path to the JSON file.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for the pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=1.5)),
    hole=0,
    sort=False,
    direction='counterclockwise',
    rotation=-30,  # Rotate to match the visual orientation of the original chart
    textinfo='percent',
    textposition='inside',
    textfont=dict(family="Arial", size=16, color='black'),
    hoverinfo='label+percent'
)])

# Update layout for a clean and accurate look
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=18, color='black')
    ),
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    showlegend=True,
    legend=dict(
        x=0.8,
        y=0.85,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)',
        font=dict(size=14)
    ),
    margin=dict(t=80, b=40, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Derive the output filename from the input JSON path
output_path = pathlib.Path(json_path).with_suffix('.png')

# Save the figure as a high-resolution PNG image
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")