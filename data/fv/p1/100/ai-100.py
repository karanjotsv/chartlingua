import sys
import json
import pathlib
import math
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

output_filename_base = json_path.stem

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
total_value = sum(values)

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    sort=False,
    direction='clockwise',
    startangle=180,
    textinfo='none',
    hoverinfo='label+percent',
    domain=dict(x=[0.2, 0.8], y=[0.1, 0.9])
))

layout_annotations = []
center_x, center_y = 0.5, 0.5
label_radius = 0.55
arrow_tip_radius = 0.30
current_angle_deg = 180.0

for i, d in enumerate(chart_data):
    slice_angle_deg = (d['value'] / total_value) * 360
    mid_angle_deg = current_angle_deg - slice_angle_deg / 2
    mid_angle_rad = math.radians(mid_angle_deg)

    text_x = center_x + label_radius * math.cos(mid_angle_rad)
    text_y = center_y + label_radius * math.sin(mid_angle_rad)

    arrow_x = center_x + arrow_tip_radius * math.cos(mid_angle_rad)
    arrow_y = center_y + arrow_tip_radius * math.sin(mid_angle_rad)
    
    # Determine text alignment based on position
    angle_norm = mid_angle_deg % 360
    if 90 < angle_norm < 270:
        xanchor = 'right'
    else:
        xanchor = 'left'

    if 0 < angle_norm < 180:
        yanchor = 'bottom'
    else:
        yanchor = 'top'

    layout_annotations.append(go.layout.Annotation(
        x=arrow_x, y=arrow_y,
        ax=text_x, ay=text_y,
        xref="paper", yref="paper",
        axref="paper", ayref="paper",
        showarrow=True,
        arrowhead=4,
        arrowsize=1.2,
        arrowwidth=1.2,
        arrowcolor="#333333",
        text=d['label'],
        font=dict(family="Arial", size=12, color='black'),
        align='center'
    ))
    current_angle_deg -= slice_angle_deg

if texts.get('annotations'):
    for ann in texts['annotations']:
        layout_annotations.append(go.layout.Annotation(
            text=ann['text'],
            x=ann['x'],
            y=ann['y'],
            xref=ann['xref'],
            yref=ann['yref'],
            showarrow=False,
            font=dict(family="Arial", size=14, color='black'),
            bgcolor='white',
            bordercolor='black',
            borderwidth=1.5,
            borderpad=4
        ))

title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font_family="Arial",
    showlegend=False,
    paper_bgcolor='#FDFBF2',
    plot_bgcolor='#FDFBF2',
    margin=dict(l=50, r=50, t=100, b=50),
    annotations=layout_annotations
)

fig.write_image(f"{output_filename_base}.png", scale=2, width=800, height=650)

print(f"Chart saved to {output_filename_base}.png")