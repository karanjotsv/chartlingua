import sys
import json
import os
import math
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# --- 2. Extract data and configuration from JSON ---
chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', {})

main_pie_data = chart_data.get('main_pie', {})
sub_pie_data = chart_data.get('sub_pie', {})
main_pie_colors = colors.get('main_pie', [])
sub_pie_colors = colors.get('sub_pie', [])

# --- 3. Create Figure and Traces ---
fig = go.Figure()

# Add main pie chart
fig.add_trace(go.Pie(
    labels=main_pie_data.get('labels', []),
    values=main_pie_data.get('values', []),
    marker=dict(colors=main_pie_colors),
    hoverinfo='label+percent',
    textinfo='percent',
    textfont=dict(size=12, color='white'),
    domain=dict(x=[0, 0.55], y=[0.05, 0.95]),
    name='',
    sort=False,
    direction='clockwise',
    rotation=78 # Empirically adjusted to match original start position
))

# Add sub pie chart
fig.add_trace(go.Pie(
    labels=sub_pie_data.get('labels', []),
    values=sub_pie_data.get('values', []),
    marker=dict(colors=sub_pie_colors),
    hoverinfo='label+percent',
    textinfo='percent',
    textfont=dict(size=12, color='white'),
    hole=0.0,
    domain=dict(x=[0.65, 1.0], y=[0.25, 0.75]),
    name='',
    sort=False,
    direction='clockwise',
    rotation=30 # Empirically adjusted to match original start position
))

# --- 4. Calculate connector line positions ---
main_pie_domain = {'x': [0, 0.55], 'y': [0.05, 0.95]}
sub_pie_domain = {'x': [0.65, 1.0], 'y': [0.25, 0.75]}

main_values = main_pie_data.get('values', [])
total_main = sum(main_values)
others_label = "Others"

# Find the start and end angles of the "Others" slice
if others_label in main_pie_data.get('labels', []) and total_main > 0:
    others_index = main_pie_data['labels'].index(others_label)
    
    # Correct for rotation and direction
    # Rotation: 78 deg clockwise. Start is at 90-78 = 12 degrees from 3-o-clock.
    initial_rotation_rad = math.radians(90 - 78)

    cumulative_val_before = sum(main_values[:others_index])
    others_val = main_values[others_index]
    
    start_frac = cumulative_val_before / total_main
    end_frac = (cumulative_val_before + others_val) / total_main
    
    # Angle theta (radians) for a fraction f is `initial - f * 2*pi` due to clockwise direction
    theta1 = initial_rotation_rad - start_frac * 2 * math.pi
    theta2 = initial_rotation_rad - end_frac * 2 * math.pi

    # Main pie ellipse parameters
    cx1 = (main_pie_domain['x'][0] + main_pie_domain['x'][1]) / 2
    cy1 = (main_pie_domain['y'][0] + main_pie_domain['y'][1]) / 2
    rx1 = (main_pie_domain['x'][1] - main_pie_domain['x'][0]) / 2
    ry1 = (main_pie_domain['y'][1] - main_pie_domain['y'][0]) / 2

    # Points on the edge of the 'Others' slice
    p1_x = cx1 + rx1 * math.cos(theta1)
    p1_y = cy1 + ry1 * math.sin(theta1)
    p2_x = cx1 + rx1 * math.cos(theta2)
    p2_y = cy1 + ry1 * math.sin(theta2)

    # Destination points: top-left and bottom-left of sub-pie domain
    q1_x, q1_y = sub_pie_domain['x'][0], sub_pie_domain['y'][1]
    q2_x, q2_y = sub_pie_domain['x'][0], sub_pie_domain['y'][0]
    
    # Add shapes for connector lines
    fig.add_shape(type="line", xref="paper", yref="paper",
                  x0=p1_x, y0=p1_y, x1=q1_x, y1=q1_y,
                  line=dict(color="grey", width=1))
    fig.add_shape(type="line", xref="paper", yref="paper",
                  x0=p2_x, y0=p2_y, x1=q2_x, y1=q2_y,
                  line=dict(color="grey", width=1))


# --- 5. Update Layout and Final Styling ---
fig.update_layout(
    title=dict(
        text=texts.get('title', ''),
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=20, r=20, t=80, b=150),
    paper_bgcolor='white',
    plot_bgcolor='white',
    width=1000,
    height=650
)

# Hide percentage labels for 0% values in the sub pie
if len(fig.data) > 1:
    sub_pie_trace = fig.data[1]
    sub_pie_trace.text = [f'{v}%' if v > 0 else '' for v in sub_pie_trace.values]


# --- 6. Output image ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")