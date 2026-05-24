import sys
import json
import pathlib
import plotly.graph_objects as go
import math

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['category'] for item in data]
values = [item['value'] for item in data]
display_labels = [item.get('display_label', item['category']) for item in data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1.5)
    ),
    hole=0,
    direction='clockwise',
    rotation=65,
    textinfo='none',
    hoverinfo='label+percent',
    sort=False
)

fig = go.Figure(data=[pie_trace])

# Add annotations for labels outside the pie chart
annotations = []
cumulative_percent = 0
label_radius = 1.25
start_angle_deg = 65

# Convert percentages to angles and calculate mid-point for each slice
total_value = sum(values)
angles = [(v / total_value) * 360 for v in values]
mid_angles_deg = []
current_angle = start_angle_deg
for angle in angles:
    mid_angles_deg.append(current_angle - angle / 2)
    current_angle -= angle

for i, label_text in enumerate(display_labels):
    mid_angle_rad = math.radians(mid_angles_deg[i])
    x_pos = label_radius * math.cos(mid_angle_rad)
    y_pos = label_radius * math.sin(mid_angle_rad)

    # Adjust text anchor based on position to avoid overlap
    angle_norm = mid_angles_deg[i] % 360
    if 15 < angle_norm <= 165:
        yanchor = 'bottom'
    elif 195 < angle_norm <= 345:
        yanchor = 'top'
    else:
        yanchor = 'middle'

    if 105 < angle_norm <= 255:
        xanchor = 'right'
    elif angle_norm <= 75 or angle_norm > 285:
        xanchor = 'left'
    else:
        xanchor = 'center'

    annotations.append(go.layout.Annotation(
        x=x_pos,
        y=y_pos,
        text=label_text,
        showarrow=False,
        font=dict(
            family="Arial",
            size=16,
            color="#FFFFFF"
        ),
        xanchor=xanchor,
        yanchor=yanchor,
        xref="paper",
        yref="paper"
    ))

# Configure layout
title_text = texts.get('title', '')
if title_text:
    title_text = title_text.replace(', according to Gartner', ',<br>according to Gartner')

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    showlegend=False,
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(
        family="Arial",
        color="white"
    ),
    margin=dict(t=100, b=40, l=40, r=40),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    annotations=annotations
)

# Set the domain to create space for annotations
fig.update_traces(domain_x=[0.15, 0.85], domain_y=[0.15, 0.85])

output_filename_base = json_path.stem
output_png = f"{output_filename_base}.png"

fig.write_image(output_png, scale=2, width=800, height=600)
print(f"Chart saved to {output_png}")