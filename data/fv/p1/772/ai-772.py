import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Derive output filename from JSON filename
output_filename = json_file_path.with_suffix('.png')

# Load data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
colors = chart_info['colors']

# Prepare subplot specifications
rows = 4
cols = 2
specs = [[{}, {}], [{}, {}], [{}, {}], [{'colspan': 2}, None]]
subplot_titles = [chart['title'] for chart in chart_data]

# Find the maximum value across all charts for a consistent x-axis range
max_value = 0
for chart in chart_data:
    if chart['values']:
        max_value = max(max_value, max(chart['values']))

# Create subplots
fig = make_subplots(
    rows=rows,
    cols=cols,
    specs=specs,
    subplot_titles=subplot_titles,
    vertical_spacing=0.15,
    horizontal_spacing=0.1
)

# Define subplot coordinates for each chart
coords = [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2), (4, 1)]

# Add traces for each subplot
for i, chart in enumerate(chart_data):
    row, col = coords[i]
    fig.add_trace(
        go.Bar(
            x=chart['values'],
            y=chart['categories'],
            orientation='h',
            marker_color=colors[0],
            text=chart['values'],
            textposition='outside',
            textfont=dict(color=colors[0], size=12, family="Arial"),
            hoverinfo='none',
            cliponaxis=False
        ),
        row=row,
        col=col
    )

# Update the layout for a clean and accurate look
fig.update_layout(
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=200, r=50, t=50, b=50),
    height=1100,
    width=900
)

# Style subplot titles (which are annotations)
for annotation in fig.layout.annotations:
    annotation.update(
        x=0,
        xanchor='left',
        font=dict(family="Arial", size=16, color='black'),
        align='left'
    )
    # This is a bit of a hack to make the font bold, as `weight` is not a direct property
    annotation.text = f"<b>{annotation.text}</b>"


# Style all axes
fig.update_xaxes(
    showgrid=False,
    showline=False,
    showticklabels=False,
    zeroline=False,
    range=[0, max_value * 1.15] # Provide padding for outside text
)

fig.update_yaxes(
    showgrid=False,
    showline=False,
    ticks="",
    categoryorder='array', # Respect the order from the data list
    autorange=True
)

# Write the image to a file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")