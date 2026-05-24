import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data and texts from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]

# Create subplots figure
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.15,
    subplot_titles=(texts["title_top"], texts["title_bottom"])
)

# Add traces for each subplot
# Top plot
fig.add_trace(
    go.Scatter(
        x=chart_data[0]['x_values'],
        y=chart_data[0]['y_values'],
        mode='lines',
        line=dict(color=colors[0]),
        showlegend=False
    ),
    row=1, col=1
)

# Bottom plot
fig.add_trace(
    go.Scatter(
        x=chart_data[1]['x_values'],
        y=chart_data[1]['y_values'],
        mode='lines',
        line=dict(color=colors[0]),
        showlegend=False
    ),
    row=2, col=1
)

# Update layout, axes, and styling
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    height=600,
    width=800,
    margin=dict(t=80, b=80, l=80, r=40)
)

# Style axes to mimic the original chart
fig.update_xaxes(
    title_text=texts["x_axis_label"],
    row=2, col=1,
    range=[0, 40],
    showline=True, linewidth=1, linecolor='black', mirror=True,
    ticks='inside', tickcolor='black', ticklen=5,
    gridcolor='lightgrey', showgrid=False
)
# Update top y-axis
fig.update_yaxes(
    title_text=texts["y_axis_label_top"],
    row=1, col=1,
    range=[0, 10000],
    showline=True, linewidth=1, linecolor='black', mirror=True,
    ticks='inside', tickcolor='black', ticklen=5,
    gridcolor='lightgrey', showgrid=False
)

# Update bottom y-axis
fig.update_yaxes(
    title_text=texts["y_axis_label_bottom"],
    row=2, col=1,
    range=[-1000, 1000],
    showline=True, linewidth=1, linecolor='black', mirror=True,
    ticks='inside', tickcolor='black', ticklen=5,
    gridcolor='lightgrey', showgrid=False
)

# Set subplot title font size
for annotation in fig.layout.annotations:
    annotation.font.size = 12

# Generate the output image file
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")