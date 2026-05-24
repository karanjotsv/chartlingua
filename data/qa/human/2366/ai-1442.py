import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from command-line argument
json_filepath = Path(sys.argv[1])

# Read the JSON data
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_filepath}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_filepath}")
    sys.exit(1)

# Extract data and texts from the JSON object
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0] if colors else None,
    text=[f'{v:,}'.replace(',', ' ') for v in values],
    textposition='auto',
    insidetextanchor='end',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Update layout
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        griddash='dot',
        zeroline=False,
        showline=False,
        tickvals=[i * 100000 for i in range(13)],
        ticktext=[f'{i * 100000:,}'.replace(',', ' ') for i in range(13)],
        range=[0, 1250000]
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showline=True,
        linecolor='black',
        linewidth=1,
        autorange="reversed" # This ensures the first category in the list is at the top
    ),
    margin=dict(l=100, r=80, t=50, b=80),
    showlegend=False
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.15,
        xanchor='right',
        yanchor='top'
    )

# Define output filename and save the image
output_filename = json_filepath.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")