import sys
import json
import math
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]
output_filename_base = Path(json_path).stem

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}", file=sys.stderr)
    sys.exit(1)

data_series = chart_info['chart_data']
subplot_titles = [d['title'] for d in data_series]

fig = make_subplots(rows=1, cols=2,
                    specs=[[{'type': 'domain'}, {'type': 'domain'}]],
                    subplot_titles=subplot_titles)

annotations = []
total_charts = len(data_series)

for i, chart in enumerate(data_series):
    col = i + 1
    labels = chart['labels']
    values = chart['values']
    colors = chart['colors']
    text_info = chart['text_info']
    rotation = chart.get('rotation', 0)

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker_colors=colors,
        textinfo='none',
        hoverinfo='label+percent',
        sort=False,
        direction='clockwise',
        rotation=rotation
    ), row=1, col=col)

    # Calculate positions for slice label annotations
    total_value = sum(values)
    current_angle_deg = rotation
    annot_radius_factor = 0.6  # 0-1, distance from center

    # Subplot domain info
    domain_x = [i / total_charts, (i + 1) / total_charts]
    center_x = (domain_x[0] + domain_x[1]) / 2
    center_y = 0.5
    radius_x = (domain_x[1] - domain_x[0]) / 2
    
    # Pie charts are circular, so we can use the smaller radius to avoid distortion
    # Assuming height is larger than subplot width
    effective_radius = radius_x 

    for j, val in enumerate(values):
        angle_deg = (val / total_value) * 360
        mid_angle_deg = current_angle_deg - (angle_deg / 2)
        mid_angle_rad = math.radians(mid_angle_deg)

        annot_x = center_x + effective_radius * annot_radius_factor * math.cos(mid_angle_rad)
        annot_y = center_y + effective_radius * annot_radius_factor * math.sin(mid_angle_rad)

        annotations.append(dict(
            x=annot_x,
            y=annot_y,
            text=f"{labels[j].upper()}<br>{val}%",
            showarrow=False,
            font=dict(color='white', family="Arial", size=11),
            bgcolor='#2c2c2c',
            borderpad=4,
            xref='paper',
            yref='paper',
            xanchor='center',
            yanchor='middle'
        ))
        current_angle_deg -= angle_deg

    # Annotation for text_info below the chart
    annotations.append(dict(
        x=center_x,
        y=0.1,  # Position below the chart
        text=text_info,
        showarrow=False,
        font=dict(family="Arial", size=12, color='#333333'),
        align='center',
        xanchor='center',
        yanchor='top',
        xref='paper',
        yref='paper'
    ))

# Source annotation
annotations.append(dict(
    x=0.99,
    y=0.01,
    text=chart_info['texts']['source'],
    showarrow=False,
    font=dict(family="Arial", size=10, color='#555555'),
    align='right',
    xanchor='right',
    yanchor='bottom',
    xref='paper',
    yref='paper'
))

fig.update_layout(
    annotations=annotations,
    showlegend=False,
    paper_bgcolor='#e8e8e8',
    plot_bgcolor='#e8e8e8',
    margin=dict(l=20, r=20, t=60, b=120),
    height=560,
    width=932,
    font=dict(family="Arial", color='#333333')
)

# Style subplot titles
for i in fig['layout']['annotations']:
    if i['text'] in subplot_titles:
        i['font'] = dict(family='Arial', size=16, color='#333333')
        i['y'] = 0.95 # Adjust vertical position

output_file = f"{output_filename_base}.png"
fig.write_image(output_file, scale=2)
print(f"Chart saved to {output_file}")