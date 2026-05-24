import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Verify the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_file_path}'")
    sys.exit(1)

# Extract data and texts from the JSON object
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Create the figure
fig = go.Figure()

# Add bar trace
if data_series:
    series = data_series[0]
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        text=series['y'],
        textposition='outside',
        cliponaxis=False,
        marker_color=colors[0] if colors else None,
        name=series.get('name', '')
    ))

# Update layout
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 300],
        gridcolor='#e0e0e0',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(t=50, b=80, l=80, r=40),
    annotations=[
        dict(
            text=texts.get('source', ''),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.2,
            xanchor='right',
            yanchor='bottom'
        )
    ]
)

# Define output path for the PNG file
output_png_path = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
try:
    fig.write_image(output_png_path, scale=2)
    print(f"Chart saved to {output_png_path}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)