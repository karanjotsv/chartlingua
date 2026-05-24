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
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

output_filename = json_path.with_suffix(".png")

with open(json_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

chart_data = chart_json['chart_data']
texts = chart_json['texts']
colors = chart_json['colors']

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
total_value = sum(values)

# This rotation value is estimated to align the chart as in the original image,
# where the boundary between the largest and second-to-last slice is at ~10 o'clock.
rotation = 150

pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='black', width=1)),
    sort=False,
    direction='clockwise',
    rotation=rotation,
    textinfo='none',
    hoverinfo='label+percent'
)

annotations = []
cumulative_angle_deg = rotation
small_slices_labels = ['COLOMBIA', 'KAZAKHSTAN', 'POLAND']

for item in chart_data:
    slice_angle_deg = (item['value'] / total_value) * 360
    mid_angle_deg = cumulative_angle_deg + (slice_angle_deg / 2)
    mid_angle_rad = math.radians(mid_angle_deg)
    cumulative_angle_deg += slice_angle_deg

    # Annotation for the outer labels
    r_outer = 1.08
    x_outer = r_outer * math.cos(mid_angle_rad)
    y_outer = r_outer * math.sin(mid_angle_rad)

    if item['label'] in small_slices_labels:
        label_text = f"{item['value']} {item['label']}"
    else:
        label_text = item['label']

    if math.isclose(math.cos(mid_angle_rad), 0, abs_tol=1e-2):
        xanchor = 'center'
    elif math.cos(mid_angle_rad) > 0:
        xanchor = 'left'
    else:
        xanchor = 'right'

    annotations.append(
        go.layout.Annotation(
            x=x_outer, y=y_outer, text=label_text, showarrow=False,
            font=dict(family="Arial", size=12, color="black"),
            xanchor=xanchor, yanchor='middle'
        )
    )

    # Annotation for the inner values on larger slices
    if item['label'] not in small_slices_labels:
        r_inner = 0.4 if item['value'] > 2000 else 0.65
        x_inner = r_inner * math.cos(mid_angle_rad)
        y_inner = r_inner * math.sin(mid_angle_rad)
        
        annotations.append(
            go.layout.Annotation(
                x=x_inner, y=y_inner, text=f"<b>{item['value']}</b>", showarrow=False,
                font=dict(family="Arial", size=14, color="#00FFFF")
            )
        )

layout = go.Layout(
    title=dict(
        text=f"<b>{texts['title']}</b>",
        y=0.98, x=0.5, xanchor='center', yanchor='top',
        font=dict(family="Arial", size=16, color="black")
    ),
    showlegend=False,
    annotations=annotations,
    xaxis=dict(showgrid=False, zeroline=False, visible=False, range=[-1.6, 1.6]),
    yaxis=dict(showgrid=False, zeroline=False, visible=False, range=[-1.4, 1.4], scaleanchor="x", scaleratio=1),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=100, b=40, l=40, r=40),
    autosize=False,
    width=800,
    height=700
)

fig = go.Figure(data=[pie_trace], layout=layout)

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")