import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get file path from command-line argument
json_path = pathlib.Path(sys.argv[1])

# Verify the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data from the JSON structure
data_series = chart_data.get("chart_data", [])
texts = chart_data.get("texts", {})
colors = chart_data.get("colors", [])
shapes = chart_data.get("shapes", [])
annotations = chart_data.get("annotations", [])
layout_options = chart_data.get("layout_options", {})

# Initialize the figure
fig = go.Figure()

# Add data series to the figure
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        mode='lines',
        name=series.get("name", ""),
        line=dict(color=colors[i % len(colors)], width=2.5),
        showlegend=False
    ))

# Update layout with titles, fonts, and other settings
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(size=24)
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=16, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=100, b=80),
    shapes=shapes,
    annotations=annotations
)

# Update axes properties based on layout_options
fig.update_xaxes(
    range=layout_options.get('x_range'),
    tickvals=layout_options.get('x_ticks'),
    showline=True,
    linewidth=1.5,
    linecolor='black',
    mirror=True,
    ticks='inside',
    tickwidth=1.5,
    tickcolor='black',
    ticklen=8,
    showgrid=False,
    zeroline=False
)

fig.update_yaxes(
    range=layout_options.get('y_range'),
    tickvals=layout_options.get('y_ticks'),
    showline=True,
    linewidth=1.5,
    linecolor='black',
    mirror=True,
    ticks='inside',
    tickwidth=1.5,
    tickcolor='black',
    ticklen=8,
    showgrid=False,
    zeroline=False
)

# Generate the output PNG file
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as '{output_filename}'")