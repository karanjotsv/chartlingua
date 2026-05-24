import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])

# Check if the file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data from the file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (json.JSONDecodeError, IOError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for plotting
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure object
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    marker_color=colors[0] if colors else '#1f77b4',
    cliponaxis=False
))

# Configure the layout based on JSON and visual analysis
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linecolor='black',
        linewidth=1,
        automargin=True
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 70000],
        dtick=10000,
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        zeroline=False,
        tickformat=' ',
        automargin=True
    ),
    margin=dict(l=100, r=40, t=50, b=100),
)

# Add source annotation at the bottom right
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.98,
        y=-0.2,
        font=dict(family="Arial", size=12, color="grey")
    )

# Update text font for the bar values
fig.update_traces(textfont_size=12, textfont_family="Arial")

# Determine the output filename from the input JSON path
output_filename = json_file_path.with_suffix('.png').name

# Save the figure to a PNG file with a high resolution
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)