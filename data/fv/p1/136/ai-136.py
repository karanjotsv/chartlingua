import sys
import json
import math
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
layout_constants = config['layout_constants']

fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'domain'}, {'type': 'domain'}]],
    horizontal_spacing=0.04
)

fig.add_trace(go.Pie(
    labels=chart_data[0]['labels'],
    values=chart_data[0]['values'],
    marker_colors=colors['chart1'],
    sort=False,
    direction='clockwise',
    rotation=layout_constants['pie_1_rotation'],
    hoverinfo='none',
    textinfo='none'
), 1, 1)

fig.add_trace(go.Pie(
    labels=chart_data[1]['labels'],
    values=chart_data[1]['values'],
    marker_colors=colors['chart2'],
    sort=False,
    direction='clockwise',
    rotation=layout_constants['pie_2_rotation'],
    hoverinfo='none',
    textinfo='none'
), 1, 2)

annotations = []

annotations.append(dict(
    text=f"<b>{texts['title_left']}</b>",
    x=0.235, y=1.0, xref='paper', yref='paper', yanchor='bottom',
    showarrow=False, align='center',
    font=dict(family='Arial', size=18, color=colors['text'])
))
annotations.append(dict(
    text=f"<b>{texts['title_right']}</b>",
    x=0.765, y=1.0, xref='paper', yref='paper', yanchor='bottom',
    showarrow=False, align='center',
    font=dict(family='Arial', size=18, color=colors['text'])
))

annotations.append(dict(
    text=texts['subtitle_left'],
    x=0.235, y=-0.05, xref='paper', yref='paper', yanchor='top',
    showarrow=False, align='center',
    font=dict(family='Arial', size=13, color=colors['text'])
))
annotations.append(dict(
    text=texts['subtitle_right'],
    x=0.765, y=-0.05, xref='paper', yref='paper', yanchor='top',
    showarrow=False, align='center',
    font=dict(family='Arial', size=13, color=colors['text'])
))

annotations.append(dict(
    text=texts['source'],
    x=0.99, y=-0.12, xref='paper', yref='paper',
    showarrow=False, align='right', xanchor='right', yanchor='top',
    font=dict(family='Arial', size=12, color=colors['text'])
))

rotations = [layout_constants['pie_1_rotation'], layout_constants['pie_2_rotation']]
x_refs = ['x', 'x2']
y_refs = ['y', 'y2']

for i, data in enumerate(chart_data):
    values = data['values']
    total_value = sum(values)
    current_angle_deg = rotations[i]
    
    for j, value in enumerate(values):
        slice_angle_deg = (value / total_value) * 360
        mid_angle_deg = -(current_angle_deg + slice_angle_deg / 2)
        mid_angle_rad = math.radians(mid_angle_deg)
        
        radial_pos = data['annotations'][j]['radial_pos']
        
        x_pos = 0.5 + radial_pos * math.cos(mid_angle_rad)
        y_pos = 0.5 + radial_pos * math.sin(mid_angle_rad)

        annotations.append(dict(
            text=f"<b>{data['annotations'][j]['text']}</b>",
            x=x_pos, y=y_pos, 
            xref=x_refs[i], yref=y_refs[i],
            showarrow=False, align='center',
            bgcolor=colors['annotation_bg'],
            font=dict(family='Arial', size=11, color=colors['annotation_text'])
        ))
        
        current_angle_deg += slice_angle_deg

fig.update_layout(
    annotations=annotations,
    showlegend=False,
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['background'],
    margin=dict(l=20, r=20, t=80, b=110),
    font=dict(family='Arial')
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2, width=800, height=450)

print(f"Chart saved to {output_filename}")