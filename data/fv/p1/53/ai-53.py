import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_path = sys.argv[1]

# Read the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and configurations from the JSON object
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', {})

# Create a figure with two subplots, sharing the x-axis
fig = make_subplots(rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.02,
                    row_heights=[0.7, 0.3])

# Add traces to the figure
for i, series in enumerate(chart_data):
    row_num = 1 if series.get('subplot') == 'y1' else 2
    fig.add_trace(
        go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            name=series.get('name'),
            mode='lines',
            line=dict(color=colors.get('series_colors', [])[i], width=1.5)
        ),
        row=row_num,
        col=1
    )

# Update the layout of the figure
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor=colors.get('background_color', '#ffffff'),
    paper_bgcolor=colors.get('background_color', '#ffffff'),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.0,
        xanchor="left",
        x=0.01,
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='rgba(0,0,0,0)'
    ),
    margin=dict(l=50, r=20, t=50, b=40)
)

# Update the axes' properties
grid_color = colors.get('grid_color', '#d3d3d3')

# Top subplot y-axis
fig.update_yaxes(
    range=[300, 1700],
    tick0=350,
    dtick=100,
    showgrid=True,
    gridcolor=grid_color,
    zeroline=False,
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    row=1, col=1
)

# Bottom subplot y-axis
fig.update_yaxes(
    range=[-5, 105],
    tickvals=[0, 20, 40, 60, 80, 100],
    showgrid=True,
    gridcolor=grid_color,
    zeroline=False,
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    row=2, col=1
)

# Shared x-axis (update on the bottom-most x-axis)
fig.update_xaxes(
    tickformat='%Y',
    dtick='M12',
    showgrid=True,
    gridcolor=grid_color,
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    ticks='outside',
    minor=dict(
        dtick="M1",
        ticklen=4,
        tickcolor="gray",
        showgrid=False
    )
)

# Hide x-axis labels and ticks for the top plot
fig.update_xaxes(showticklabels=False, row=1, col=1)

# Generate the output filename from the input JSON filename
output_filename = pathlib.Path(json_path).stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")