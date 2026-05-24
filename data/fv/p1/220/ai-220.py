import sys
import json
import plotly.graph_objects as go
import math

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = data['chart_data']
colors = data['colors']

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
slice_colors = colors['slices']
text_colors = colors['texts']

# Create the pie chart trace without default text
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=slice_colors,
        line=dict(color='white', width=2)
    ),
    sort=False,
    direction='clockwise',
    rotation=98, # Aligns the split between the last (Safari) and first (Android) slices with the 12 o'clock position
    textinfo='none', # We will use annotations for custom colored labels
    hole=0
)

fig = go.Figure(data=[pie_trace])

# Create custom annotations for each slice for colored labels
annotations = []
cumulative_value = 0
total_value = sum(values)
rotation_offset_deg = 98 # Must match the pie trace rotation

for i in range(len(values)):
    # Calculate the midpoint angle for the slice
    mid_point_percentage = cumulative_value + (values[i] / 2)
    mid_angle_deg = (mid_point_percentage / total_value) * 360
    
    # Convert pie angle to standard mathematical angle (radians, CCW from x-axis)
    # Plotly's rotation is CW from the 3 o'clock position.
    # Our effective 0-degree start is at 3 o'clock - rotation_offset_deg.
    # The math angle is thus (start_angle - mid_angle_deg)
    math_angle_deg = (360 - rotation_offset_deg - mid_angle_deg + 360) % 360
    math_angle_rad = math.radians(math_angle_deg)
    
    # Define position for the annotation just outside the pie
    radius = 1.45
    x_pos = radius * math.cos(math_angle_rad)
    y_pos = radius * math.sin(math_angle_rad)
    
    # Adjust text anchor based on position to prevent overlap
    if -0.1 < x_pos < 0.1:
        xanchor = 'center'
    elif x_pos >= 0.1:
        xanchor = 'left'
    else: # x_pos <= -0.1
        xanchor = 'right'

    if y_pos > 0.8:
        yanchor = 'bottom'
    elif y_pos < -0.8:
        yanchor = 'top'
    else:
        yanchor = 'middle'


    annotations.append(go.layout.Annotation(
        x=x_pos,
        y=y_pos,
        text=f"<b>{labels[i]}</b><br>{values[i]}%",
        showarrow=False,
        font=dict(
            family="Arial",
            size=16,
            color=text_colors[i]
        ),
        align='center',
        xanchor=xanchor,
        yanchor=yanchor,
    ))
    
    cumulative_value += values[i]

# Update layout with annotations and styling
fig.update_layout(
    showlegend=False,
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(family="Arial"),
    margin=dict(t=40, b=40, l=40, r=40),
    annotations=annotations,
    # Lock the aspect ratio to ensure the pie is a circle
    yaxis=dict(scaleanchor="x", scaleratio=1),
    xaxis=dict(constrain="domain")
)

# Derive output filename from the input JSON path
filename_base = json_path.rsplit('.', 1)[0]
output_filename = f"{filename_base}.png"

# Write image to file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")