import sys
import json
import plotly.graph_objects as go
from pathlib import Path
import math

# --- 1. Argument Parsing and File Handling ---
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}", file=sys.stderr)
    sys.exit(1)

output_path = json_path.with_suffix(".png")

# --- 2. JSON Data Loading ---
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (json.JSONDecodeError, IOError) as e:
    print(f"Error reading or parsing JSON file: {e}", file=sys.stderr)
    sys.exit(1)

# --- 3. Data Extraction ---
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [d.get('language', '') for d in chart_data]
values = [d.get('speakers', 0) for d in chart_data]
annotation_labels = [d.get('label', '') for d in chart_data]
total_value = sum(values)

# --- 4. Chart Creation ---
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1.5)),
    sort=False,
    direction='counterclockwise',
    textinfo='none',
    hoverinfo='label+percent+value',
    domain=dict(x=[0.05, 0.75], y=[0.05, 0.95]) # Make space for legend and labels
))

# --- 5. Layout and Styling ---
title_text = f"<b>{texts.get('title', '')}</b>"
subtitle = texts.get('subtitle')
if subtitle:
    title_text += f"<br><span style='font-size:12px;'>{subtitle}</span>"

fig.update_layout(
    title=dict(text=title_text, x=0.5, y=0.97, xanchor='center', yanchor='top'),
    font=dict(family="Arial", size=12),
    showlegend=True,
    legend=dict(x=0.8, y=0.8, xanchor='left', yanchor='top', font=dict(size=11)),
    margin=dict(t=120, b=40, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# --- 6. Annotations for Labels ---
annotations = []
start_angle = 0
pie_center_x = 0.40 # Approximate center of the pie's domain [0.05, 0.75]
pie_center_y = 0.50 # Approximate center of the pie's domain [0.05, 0.95]
pie_radius = 0.35   # Approximate radius of the pie in its domain

for i in range(len(values)):
    proportion = values[i] / total_value
    slice_angle = proportion * 360
    mid_angle_deg = start_angle + slice_angle / 2
    start_angle += slice_angle

    # Convert Plotly angle (degrees, 0 at 3 o'clock, clockwise) to standard math angle
    # (radians, 0 at 3 o'clock, counter-clockwise) for trigonometry.
    mid_angle_rad = math.radians(-mid_angle_deg)
    
    # Determine annotation properties based on slice size
    if proportion > 0.4:  # For the largest slice (e.g., Turkish)
        text_radius = pie_radius * 0.5
        x_pos = pie_center_x + text_radius * math.cos(mid_angle_rad)
        y_pos = pie_center_y + text_radius * math.sin(mid_angle_rad)
        annotations.append(dict(
            x=x_pos, y=y_pos, text=annotation_labels[i], showarrow=False,
            font=dict(size=10, color='white'), xanchor='center'
        ))
    elif 0.03 < proportion <= 0.4: # For medium slices
        text_radius = pie_radius + 0.1
        x_pos = pie_center_x + text_radius * math.cos(mid_angle_rad)
        y_pos = pie_center_y + text_radius * math.sin(mid_angle_rad)
        annotations.append(dict(
            x=x_pos, y=y_pos, text=annotation_labels[i], showarrow=False,
            font=dict(size=10), xanchor='center'
        ))
    else: # For small slices with leader lines
        text_radius = pie_radius + 0.18
        arrow_ref_radius = pie_radius + 0.02
        
        x_pos = pie_center_x + text_radius * math.cos(mid_angle_rad)
        y_pos = pie_center_y + text_radius * math.sin(mid_angle_rad)
        
        ax_pos = pie_center_x + arrow_ref_radius * math.cos(mid_angle_rad)
        ay_pos = pie_center_y + arrow_ref_radius * math.sin(mid_angle_rad)
        
        # Adjust text anchor based on position
        if 90 < mid_angle_deg < 270:
            xanchor = 'right'
            horizontal_shift = -0.05
        else:
            xanchor = 'left'
            horizontal_shift = 0.05

        annotations.append(dict(
            x=x_pos + horizontal_shift, y=y_pos, ax=ax_pos, ay=ay_pos,
            text=annotation_labels[i], showarrow=True, arrowhead=0,
            font=dict(size=10), xanchor=xanchor, yanchor='middle', align='left'
        ))

fig.update_layout(annotations=annotations)

# --- 7. Output ---
try:
    fig.write_image(output_path, scale=2, width=800, height=600)
    print(f"Chart saved to {output_path}")
except Exception as e:
    print(f"Error writing image file: {e}", file=sys.stderr)
    sys.exit(1)