import sys
import json
import plotly.graph_objects as go
import math

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
colors = config['colors']
texts_data = config['texts']

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
total_value = sum(values)

text_list = []
text_font_colors = []
outside_label_indices = []

for i, d in enumerate(chart_data):
    label = d['label']
    value = d['value']
    style = d.get('label_style', 'default')

    if style == 'inside_multiline':
        text_list.append(f"<b>{label}<br>{value}</b>")
    elif style == 'inside_singleline':
        text_list.append(f"<b>{label} {value}</b>")
    else:
        text_list.append(f"<b>{value}</b>")

    if style in ['outside', 'outside_special']:
        outside_label_indices.append(i)

    if label == 'NKP':
        text_font_colors.append('white')
    else:
        text_font_colors.append('black')

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.5,
    marker=dict(colors=colors, line=dict(color='white', width=2)),
    text=text_list,
    textinfo='text',
    textposition='inside',
    insidetextfont=dict(family="Arial", size=18, color=text_font_colors),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=75
)])

annotations = []
start_angle_deg = 75
current_angle_deg = start_angle_deg

for i in range(len(values)):
    slice_angle_deg = (values[i] / total_value) * 360
    mid_angle_deg = current_angle_deg - (slice_angle_deg / 2)

    if i in outside_label_indices:
        label_text = labels[i]
        style = chart_data[i].get('label_style')
        mid_angle_rad = math.radians(mid_angle_deg)

        arrow_r = 0.65
        ax_pos = arrow_r * math.cos(mid_angle_rad)
        ay_pos = arrow_r * math.sin(mid_angle_rad)

        if style == 'outside_special' and label_text == 'Independents':
            x_pos, y_pos = 0.45, 1.1
            align, xanchor = 'left', 'left'
        else:
            label_r = 1.35
            x_pos = label_r * math.cos(mid_angle_rad)
            y_pos = label_r * math.sin(mid_angle_rad)
            align = 'right' if x_pos < 0 else 'left'
            xanchor = 'right' if x_pos < 0 else 'left'

        annotations.append(go.layout.Annotation(
            x=x_pos, y=y_pos,
            text=f"<b>{label_text}</b>",
            showarrow=True, arrowhead=0,
            ax=ax_pos, ay=ay_pos,
            arrowcolor="#808080", arrowwidth=2,
            font=dict(family="Arial", size=18, color="black"),
            align=align, xanchor=xanchor
        ))
    current_angle_deg -= slice_angle_deg

fig.update_layout(
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(l=100, r=100, t=50, b=50),
    annotations=annotations,
    paper_bgcolor='white',
    plot_bgcolor='white',
    xaxis=dict(range=[-1.5, 1.5], visible=False),
    yaxis=dict(range=[-1.5, 1.5], visible=False, scaleanchor="x", scaleratio=1)
)

base_filename = json_file_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")