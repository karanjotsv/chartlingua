import sys
import json
import plotly.graph_objects as go
import pathlib

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists before proceeding.
if not pathlib.Path(json_path).is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data and configuration from the specified JSON file.
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded configuration.
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure.
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    hoverinfo='label+percent',
    textinfo='value',
    texttemplate='%{value}%',
    textposition='outside',
    sort=False,
    direction='clockwise',
    rotation=90 # Start the first slice at the top
))

# Update the layout of the figure.
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        xanchor='center',
        font=dict(family="Arial", size=18, color='black')
    ),
    legend=dict(
        x=0.8,
        y=0.8,
        xanchor='left',
        yanchor='top',
        traceorder='normal',
        font=dict(family="Arial", size=12, color='black'),
        bgcolor='rgba(0,0,0,0)',
        borderwidth=0
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=40, r=40, t=80, b=80),
    showlegend=True
)

# Add source annotation if it exists.
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.98,
        y=0.02,
        xanchor='right',
        yanchor='bottom',
        font=dict(family="Arial", size=12, color='black')
    )

# Determine the output filename from the input JSON path.
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image.
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")