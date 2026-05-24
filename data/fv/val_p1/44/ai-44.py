import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# The JSON file path is taken from the command-line argument.
json_path = sys.argv[1]
# The base name for the output PNG file is derived from the JSON filename.
output_filename_base = Path(json_path).stem

# Read and parse the JSON file.
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data and text from the loaded JSON.
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data series for Plotly.
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure object.
fig = go.Figure()

# Add the bar trace to the figure.
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors,
    text=texts.get('data_labels'),
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    hoverinfo='none',
    cliponaxis=False # Ensures text labels are not clipped by the plot area
))

# Configure the layout of the chart.
fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b>",
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(
            family="Arial",
            size=20
        )
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showline=True,
        linewidth=1,
        linecolor='#D3D3D3', # Light grey for axis line
        showgrid=False,
        automargin=True
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 60],
        showline=False,
        gridcolor='#D3D3D3', # Light grey for grid lines
        zeroline=False,
        automargin=True
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=90, b=90, l=80, r=40)
)

# Define the output file path.
output_path = f"{output_filename_base}.png"
# Write the figure to a PNG image file with a high resolution.
fig.write_image(output_path, scale=2)

print(f"Chart successfully generated and saved to '{output_path}'")