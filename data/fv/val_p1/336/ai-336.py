import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a command-line argument for the JSON file path is provided
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Read the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Load the chart data and configuration from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Initialize the Plotly figure
fig = go.Figure()

# Add the bar trace to the figure using a multi-category x-axis
fig.add_trace(go.Bar(
    x=[chart_data['x_level1'], chart_data['x_level2']],
    y=chart_data['values'],
    marker_color=colors[0],
    name='' # Hide from legend
))

# Configure the layout of the chart
fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    title_font=dict(
        family="Arial",
        size=18,
        color='black'
    ),
    xaxis=dict(
        showgrid=False,
        tickfont=dict(family="Arial", size=11),
        showline=False
    ),
    yaxis=dict(
        range=[0, 25000],
        dtick=5000,
        showgrid=True,
        gridcolor='lightgrey',
        gridwidth=1,
        tickfont=dict(family="Arial", size=11)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial"
    ),
    showlegend=False,
    margin=dict(t=80, b=80, l=60, r=40),
    bargap=0.3
)

# Add vertical lines to visually separate the main project categories on the x-axis
for i in range(1, len(set(chart_data['x_level1']))):
    fig.add_vline(
        x=(i * 2) - 0.5,
        line_width=1,
        line_color="black"
    )

# Determine the output filename from the input JSON filename
output_filename = json_file_path.stem + ".png"

# Write the figure to a PNG image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")