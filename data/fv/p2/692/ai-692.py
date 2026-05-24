import sys
import json
import math
import plotly.graph_objects as go

# 1. Load data from JSON file provided as a command-line argument
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
slice_colors = config['colors']['slices']
text_colors = config['colors']['texts']

# 2. Prepare data for Plotly
labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

# 3. Create the pie chart trace
fig = go.Figure()

# Set rotation to place the 'HYDRO' slice in the top-left quadrant and direction to clockwise
# to match the original image's layout and data order.
start_rotation_deg = 140
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=slice_colors, line=dict(color='#FFFFFF', width=2)),
    textinfo='none',  # Disable default text to use custom annotations
    sort=False,
    direction='clockwise',
    rotation=start_rotation_deg
))

# 4. Add custom labels as annotations for precise color and placement control
total_value = sum(values)
current_sum = 0
radius_factor = 0.65  # Controls distance of labels from the pie's center

for i, d in enumerate(chart_data):
    # Calculate the midpoint angle of the slice in degrees
    mid_angle_deg = start_rotation_deg - (current_sum + d['value'] / 2) / total_value * 360
    mid_angle_rad = math.radians(mid_angle_deg)

    # Position annotation based on the angle and radius
    x_pos = 0.5 + radius_factor * math.cos(mid_angle_rad)
    y_pos = 0.5 + radius_factor * math.sin(mid_angle_rad)

    # Adjust text anchor based on which side of the chart it is on for better alignment
    xanchor = 'left' if x_pos > 0.5 else 'right'
    yanchor = 'middle'

    fig.add_annotation(
        x=x_pos,
        y=y_pos,
        text=f"{d['label']}<br>{d['value']}%",
        showarrow=False,
        font=dict(family="Arial", size=12, color=text_colors[i]),
        xanchor=xanchor,
        yanchor=yanchor,
        xref="paper",
        yref="paper"
    )
    current_sum += d['value']

# 5. Configure overall layout and styling
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(family="Arial", size=14),
    showlegend=False,
    margin=dict(t=100, b=50, l=50, r=50),
    paper_bgcolor='white',
    # Hide axis lines that can appear when using paper-referenced annotations
    xaxis=dict(visible=False),
    yaxis=dict(visible=False)
)

# 6. Save the output image
base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")