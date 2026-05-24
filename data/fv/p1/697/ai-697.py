import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])

# Check if the provided path is a valid file
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read and load the JSON data from the file
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Determine the output image path from the input JSON path
output_path = json_path.with_suffix('.png')

# Initialize a Figure object
fig = go.Figure()

# Define a consistent bar width for calculations
bar_width = 0.8

# Add the bar chart trace
fig.add_trace(go.Bar(
    x=data['chart_data']['x'],
    y=data['chart_data']['y'],
    marker_color=data['colors']['bars'],
    marker_line_width=0,
    width=bar_width,
    showlegend=False
))

# Calculate the x-coordinates for the water area rectangle based on bar indices
start_bar_x = data['chart_data']['x'][data['water_area']['start_bar_index']]
end_bar_x = data['chart_data']['x'][data['water_area']['end_bar_index']]
rect_x0 = start_bar_x - (bar_width / 2)
rect_x1 = end_bar_x + (bar_width / 2)

# Add the water area as a rectangle shape, layered below the bars
fig.add_shape(
    type="rect",
    x0=rect_x0,
    y0=0,
    x1=rect_x1,
    y1=data['water_area']['y_level'],
    fillcolor=data['water_area']['color'],
    line_width=0,
    layer='below'
)

# Configure the layout of the chart
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        range=[0.5, 9.5]
    ),
    yaxis=dict(
        title_text=None,
        tickvals=list(range(9)),
        tickfont=dict(size=14),
        showgrid=False,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        range=[0, 8.5]
    ),
    margin=dict(l=40, r=10, t=10, b=20)
)

# Write the generated figure to a PNG image file
fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")