import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get file path from command-line argument
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract titles for subplots
subplot_titles = [subplot['title'] for subplot in data['subplots']]

# Create a figure with subplots
fig = make_subplots(rows=len(data['subplots']), cols=1, subplot_titles=subplot_titles)

# Iterate through each subplot's data and add traces
for i, subplot_data in enumerate(data['subplots']):
    for j, series in enumerate(subplot_data['chart_data']):
        fig.add_trace(
            go.Scatter(
                x=series['x'],
                y=series['y'],
                name=series['name'],
                mode='lines',
                line=dict(color=data['colors']['series_colors'][j]),
                legendgroup=series['name'],
                showlegend=(i == 0) # Show legend only for the first subplot
            ),
            row=i + 1,
            col=1
        )

# Update layout for the entire figure
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    legend=dict(
        x=0.65,
        y=0.9,
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=60, r=40, t=50, b=50)
)

# Update all x-axes and y-axes with shared properties
fig.update_xaxes(
    title_text=data['texts']['x_axis_title'],
    range=[10, 16],
    dtick=1,
    showgrid=True,
    gridwidth=1,
    gridcolor='LightGray',
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True
)

fig.update_yaxes(
    title_text=data['texts']['y_axis_title'],
    range=[0, 18],
    dtick=2,
    showgrid=True,
    gridwidth=1,
    gridcolor='LightGray',
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True
)

# Define output filename from the input JSON filename
output_filename = json_path.stem + ".png"

# Save the figure to a file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")