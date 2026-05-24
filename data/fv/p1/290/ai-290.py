import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
data = chart_data.get("chart_data", [])
texts = chart_data.get("texts", {})
colors = chart_data.get("colors", [])

# Create subplots figure
fig = make_subplots(
    rows=2,
    cols=1,
    subplot_titles=(texts.get("title_top"), texts.get("title_bottom")),
    vertical_spacing=0.15
)

color_idx = 0

# Add trace for the top subplot
if len(data) > 0:
    subplot1_data = data[0]
    for series in subplot1_data.get("series", []):
        fig.add_trace(
            go.Scatter(
                x=subplot1_data.get("x_values"),
                y=series.get("y_values"),
                mode='lines',
                line=dict(color=colors[color_idx] if color_idx < len(colors) else None),
                showlegend=False
            ),
            row=1, col=1
        )
        color_idx += 1

# Add traces for the bottom subplot
if len(data) > 1:
    subplot2_data = data[1]
    for series in subplot2_data.get("series", []):
        fig.add_trace(
            go.Scatter(
                x=subplot2_data.get("x_values"),
                y=series.get("y_values"),
                name=series.get("name"),
                mode='lines',
                line=dict(color=colors[color_idx] if color_idx < len(colors) else None)
            ),
            row=2, col=1
        )
        color_idx += 1

# Update layout and axes
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    height=600,
    width=800,
    margin=dict(l=80, r=40, t=80, b=80),
    legend=dict(
        x=0.95, y=0.45,
        xanchor='right', yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    )
)

# Update axes for top subplot
fig.update_yaxes(
    title_text=texts.get("y_axis_label_top"),
    range=[0, 10000],
    row=1, col=1,
    gridcolor='lightgray',
    mirror=True, ticks='outside', showline=True, linecolor='black'
)
fig.update_xaxes(
    title_text=texts.get("x_axis_label_top"),
    range=[0, 40],
    row=1, col=1,
    gridcolor='lightgray',
    mirror=True, ticks='outside', showline=True, linecolor='black'
)

# Update axes for bottom subplot
fig.update_yaxes(
    title_text=texts.get("y_axis_label_bottom"),
    range=[-200, 1400],
    row=2, col=1,
    gridcolor='lightgray',
    mirror=True, ticks='outside', showline=True, linecolor='black'
)
fig.update_xaxes(
    title_text=texts.get("x_axis_label_bottom"),
    range=[0, 40],
    row=2, col=1,
    gridcolor='lightgray',
    mirror=True, ticks='outside', showline=True, linecolor='black'
)

# Generate output filename and save the image
output_filename = pathlib.Path(json_path).stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")