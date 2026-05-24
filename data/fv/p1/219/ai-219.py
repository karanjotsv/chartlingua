import sys
import json
import plotly.graph_objects as go
import math

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and settings from the JSON object
chart_data = chart_info.get("chart_data", [])
colors_data = chart_info.get("colors", {})
texts = chart_info.get("texts", {})

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

slice_colors = colors_data.get("slices", [])
label_colors = colors_data.get("labels", [])
background_color = colors_data.get("background", "#FFFFFF")
pie_border_color = colors_data.get("pie_border", "#000000")

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=slice_colors,
        line=dict(color=pie_border_color, width=2)
    ),
    sort=False,
    direction='clockwise',
    rotation=90,
    textinfo='none',
    hoverinfo='label+percent'
)

fig = go.Figure(data=[pie_trace])

# Create annotations for labels outside the pie
annotations = []
total_value = sum(values)
current_angle_deg = 90  # Start from the top (North)
radius = 0.8 # Radius for annotation placement relative to pie radius of 1

for i, item in enumerate(chart_data):
    slice_angle_deg = (item['value'] / total_value) * 360
    mid_angle_deg = current_angle_deg - (slice_angle_deg / 2)
    
    mid_angle_rad = math.radians(mid_angle_deg)
    
    # Position annotations just outside the pie
    x_pos = radius * math.cos(mid_angle_rad)
    y_pos = radius * math.sin(mid_angle_rad)
    
    # Determine text anchor based on position
    if -45 <= mid_angle_deg <= 45: # Right
        xanchor = 'left'
        yanchor = 'middle'
    elif 45 < mid_angle_deg < 135: # Top
        xanchor = 'center'
        yanchor = 'bottom'
    elif 135 <= mid_angle_deg <= 225: # Left
        xanchor = 'right'
        yanchor = 'middle'
    else: # Bottom
        xanchor = 'center'
        yanchor = 'top'

    annotation_text = f"<b>{item['label']}</b><br>{item['value']}%"
    
    annotations.append(
        dict(
            x=x_pos,
            y=y_pos,
            text=annotation_text,
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
    current_angle_deg -= slice_angle_deg

# Update layout
fig.update_layout(
    showlegend=False,
    paper_bgcolor=background_color,
    plot_bgcolor=background_color,
    font=dict(family="Arial"),
    annotations=annotations,
    margin=dict(t=30, b=30, l=30, r=30),
    # Ensure the pie is a circle
    yaxis=dict(scaleanchor="x", scaleratio=1)
)

# Derive output filename from the input JSON filename
if '/' in json_path:
    filename_base = json_path.split('/')[-1].rsplit('.', 1)[0]
elif '\\' in json_path:
    filename_base = json_path.split('\\')[-1].rsplit('.', 1)[0]
else:
    filename_base = json_path.rsplit('.', 1)[0]

output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2, width=600, height=600)

print(f"Chart saved to {output_filename}")