import sys
import json
import os
import math
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

fig = go.Figure()

# Define domains for the two pie charts
domain1 = {'x': [0.0, 0.48], 'y': [0.0, 1.0]}
domain2 = {'x': [0.52, 1.0], 'y': [0.0, 1.0]}

# Main pie chart
fig.add_trace(go.Pie(
    labels=config['chart_data']['main_pie']['labels'],
    values=config['chart_data']['main_pie']['values'],
    marker_colors=config['colors']['main_pie_slices'],
    textfont=dict(color=config['colors']['main_pie_text'], size=14),
    hoverinfo='label+percent',
    textinfo='text',
    texttemplate='%{label}<br>%{value}%',
    textposition='inside',
    domain=domain1,
    sort=False,
    direction='clockwise',
    rotation=180
))

# Sub pie chart
fig.add_trace(go.Pie(
    labels=config['chart_data']['sub_pie']['labels'],
    values=config['chart_data']['sub_pie']['values'],
    marker_colors=config['colors']['sub_pie_slices'],
    textfont=dict(color=config['colors']['sub_pie_text'], size=14),
    hoverinfo='label+percent',
    textinfo='text',
    texttemplate='%{label}<br>%{value:.1f}%',
    textposition='inside',
    domain=domain2,
    sort=False,
    direction='clockwise',
    rotation=107
))

# --- Calculate and add connector lines ---
# Find the 'Renewables' slice to connect from
renew_index = -1
try:
    renew_index = config['chart_data']['main_pie']['labels'].index('Renewables')
except ValueError:
    pass # If label not found, no lines will be drawn

shapes = []
if renew_index != -1:
    # Calculate angles for the 'Renewables' slice in the main pie
    values1 = config['chart_data']['main_pie']['values']
    total_val1 = sum(values1)
    rotation1 = 180
    
    current_angle = rotation1
    renew_start_angle = 0
    renew_end_angle = 0

    for i, val in enumerate(values1):
        slice_angle = (val / total_val1) * 360
        start_angle = current_angle
        end_angle = current_angle - slice_angle
        if i == renew_index:
            renew_start_angle = start_angle
            renew_end_angle = end_angle
            break
        current_angle = end_angle

    # Convert angles to radians
    angle_top_rad = math.radians(renew_start_angle)
    angle_bottom_rad = math.radians(renew_end_angle)
    
    # Main pie center and radii (in paper coordinates)
    x_center1 = (domain1['x'][0] + domain1['x'][1]) / 2
    y_center1 = (domain1['y'][0] + domain1['y'][1]) / 2
    x_radius1 = (domain1['x'][1] - domain1['x'][0]) / 2
    y_radius1 = (domain1['y'][1] - domain1['y'][0]) / 2

    # Points on the circumference of the main pie
    p1_x = x_center1 + x_radius1 * math.cos(angle_top_rad)
    p1_y = y_center1 + y_radius1 * math.sin(angle_top_rad)
    p2_x = x_center1 + x_radius1 * math.cos(angle_bottom_rad)
    p2_y = y_center1 + y_radius1 * math.sin(angle_bottom_rad)
    
    # Sub pie center and radii
    x_center2 = (domain2['x'][0] + domain2['x'][1]) / 2
    y_center2 = (domain2['y'][0] + domain2['y'][1]) / 2
    x_radius2 = (domain2['x'][1] - domain2['x'][0]) / 2
    y_radius2 = (domain2['y'][1] - domain2['y'][0]) / 2

    # Points on the circumference of the sub pie
    p3_x = x_center2 - x_radius2
    p3_y = y_center2 + y_radius2 * 0.5 # Connect slightly above the equator
    p4_x = x_center2 - x_radius2
    p4_y = y_center2 - y_radius2 * 0.5 # Connect slightly below the equator
    
    shapes.append(go.layout.Shape(type="line", xref="paper", yref="paper", x0=p1_x, y0=p1_y, x1=p3_x, y1=p3_y, line=dict(color="grey", width=1)))
    shapes.append(go.layout.Shape(type="line", xref="paper", yref="paper", x0=p2_x, y0=p2_y, x1=p4_x, y1=p4_y, line=dict(color="grey", width=1)))

# Update layout
fig.update_layout(
    title_text=config['texts']['title'],
    title_x=0.5,
    font=dict(family="Arial", size=16),
    showlegend=False,
    margin=dict(t=80, b=20, l=20, r=20),
    paper_bgcolor='white',
    plot_bgcolor='white',
    shapes=shapes
)

# Output image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2, width=900, height=450)

print(f"Chart saved to {output_filename}")