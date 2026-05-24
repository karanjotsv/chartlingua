import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

chart_data = data['chart_data']
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=data['colors'][0],
    text=[f'<b>{v}%</b>' for v in values],
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12
    )
))

background_shapes = []
for i in range(len(categories)):
    if i % 2 != 0:
        shape = go.layout.Shape(
            type="rect",
            xref="x",
            yref="paper",
            x0=i - 0.5,
            y0=0,
            x1=i + 0.5,
            y1=1,
            fillcolor="#f0f0f0",
            opacity=0.5,
            layer="below",
            line_width=0,
        )
        background_shapes.append(shape)

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=data['texts']['x_axis_title'],
        showgrid=False,
        showline=False,
        ticks='',
        linecolor='black'
    ),
    yaxis=dict(
        title_text=data['texts']['y_axis_title'],
        range=[0, 41],
        dtick=5,
        ticksuffix='%',
        gridcolor='#e0e0e0',
        showgrid=True,
        showline=False,
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=60, b=120),
    showlegend=False,
    shapes=background_shapes,
    annotations=[
        dict(
            text=data['texts']['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.28,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=10, color="grey")
        )
    ]
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")