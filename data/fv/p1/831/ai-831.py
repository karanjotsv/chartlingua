import sys
import json
import os
import math
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hole=0,
    sort=False,
    direction='clockwise',
    rotation=90,
    textinfo='none',
    hoverinfo='label+percent'
)

fig = go.Figure(data=[pie_trace])

annotations = []
cumulative_value = 0
total_value = sum(values)

for i, item in enumerate(chart_data):
    mid_angle_deg = 90 - (cumulative_value + item['value'] / 2) / total_value * 360
    mid_angle_rad = math.radians(mid_angle_deg)
    
    text_radius = 1.3
    x_text = text_radius * math.cos(mid_angle_rad)
    y_text = text_radius * math.sin(mid_angle_rad)
    
    arrow_radius = 0.95
    x_arrow = arrow_radius * math.cos(mid_angle_rad)
    y_arrow = arrow_radius * math.sin(mid_angle_rad)

    align = 'left' if -90 <= mid_angle_deg <= 90 else 'right'
    if abs(x_text) < 0.2:
        align = 'center'
    
    xanchor = align
    
    annotations.append(
        dict(
            x=x_text,
            y=y_text,
            xref='x',
            yref='y',
            text=f"{item['label']}<br>{item['value']}%",
            showarrow=True,
            arrowhead=0,
            ax=x_arrow,
            ay=y_arrow,
            axref='x',
            ayref='y',
            font=dict(
                family="Arial",
                size=12,
                color="#000000"
            ),
            align=align,
            xanchor=xanchor,
            yanchor='middle'
        )
    )
    cumulative_value += item['value']

title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.98,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=20)
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    margin=dict(l=150, r=150, t=100, b=80),
    paper_bgcolor='white',
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        range=[-1.8, 1.8]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        range=[-1.6, 1.6],
        scaleanchor="x",
        scaleratio=1
    ),
    annotations=annotations
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")