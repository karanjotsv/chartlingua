import sys
import json
import math
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

# Extract data and styling information from the JSON structure
chart_data = chart_spec['chart_data']
slice_colors = chart_spec['colors']

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
label_colors = [item['label_color'] for item in chart_data]

# Create the pie chart trace
fig = go.Figure()

fig.add_trace(go.Pie(
    values=values,
    marker=dict(colors=slice_colors, line=dict(color='white', width=1.5)),
    sort=False,
    direction='clockwise',
    rotation=195,
    textinfo='none',
    pull=[0.01] * len(values)
))

# Add annotations to create custom-colored labels outside the pie
annotations = []
total_value = sum(values)
current_angle_deg = 195.0
label_radius = 1.3  # Controls the distance of labels from the pie's center

for i in range(len(values)):
    slice_share = values[i] / total_value
    slice_angle_deg = 360 * slice_share
    # Calculate the angle for the middle of the slice
    mid_angle_deg = current_angle_deg - (slice_angle_deg / 2)
    mid_angle_rad = math.radians(mid_angle_deg)

    # Calculate the (x, y) position for the annotation
    x_pos = label_radius * math.cos(mid_angle_rad)
    y_pos = label_radius * math.sin(mid_angle_rad)

    # Determine text alignment anchor based on the label's position
    if x_pos > 0.1:
        xanchor = 'left'
    elif x_pos < -0.1:
        xanchor = 'right'
    else:
        xanchor = 'center'

    if y_pos > 0.1:
        yanchor = 'bottom'
    elif y_pos < -0.1:
        yanchor = 'top'
    else:
        yanchor = 'middle'

    annotations.append(
        go.layout.Annotation(
            x=x_pos,
            y=y_pos,
            text=labels[i],
            showarrow=False,
            font=dict(
                family="Arial",
                size=16,
                color=label_colors[i]
            ),
            xanchor=xanchor,
            yanchor=yanchor
        )
    )
    # Move to the start of the next slice
    current_angle_deg -= slice_angle_deg

# Configure the layout of the figure
fig.update_layout(
    showlegend=False,
    annotations=annotations,
    # Set a fixed, square aspect ratio to ensure the pie is a circle
    # and to position annotations relative to the pie correctly.
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.7, 1.7]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.7, 1.7], scaleanchor="x", scaleratio=1),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(t=30, b=30, l=30, r=30),
    font_family="Arial"
)

# Determine the output filename from the input JSON path
base_filename = json_path.stem
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")