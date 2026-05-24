import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        name=series.get('name', ''),
        line=dict(color=colors['series'][i], width=4),
        showlegend=False
    ))

all_x = [val for series in chart_data for val in series['x']]
all_y = [val for series in chart_data for val in series['y']]
x_max = max(all_x) * 1.05
y_max = max(all_y) * 1.15

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial"),
    margin=dict(l=80, r=40, t=40, b=80),
    xaxis=dict(
        visible=False,
        range=[0, x_max]
    ),
    yaxis=dict(
        visible=False,
        range=[0, y_max]
    ),
    shapes=[
        go.layout.Shape(type="line", x0=0, y0=0, x1=x_max, y1=0, line=dict(color=colors['axes'][0], width=3)),
        go.layout.Shape(type="line", x0=0, y0=0, x1=0, y1=y_max, line=dict(color=colors['axes'][1], width=3))
    ],
    width=550,
    height=550
)

# Add series label annotations
for ann in texts.get('annotations', []):
    fig.add_annotation(
        x=ann['x'],
        y=ann['y'],
        text=ann['text'],
        showarrow=False,
        font=dict(
            family="Arial",
            size=20,
            color=colors['series'][ann['color_index']]
        )
    )

# Add axis title annotations
fig.add_annotation(
    x=x_max / 2,
    y=-y_max * 0.15,
    text=texts['x_axis_title'],
    showarrow=False,
    font=dict(size=18, color=colors['axes'][0]),
    xref="x", yref="y"
)
fig.add_annotation(
    x=-x_max * 0.15,
    y=y_max / 2,
    text=texts['y_axis_title'],
    showarrow=False,
    textangle=-90,
    font=dict(size=18, color=colors['axes'][1]),
    xref="x", yref="y"
)

# Add axis arrow annotations
fig.add_annotation(
    x=x_max, y=0, ax=-20, ay=0, showarrow=True, arrowhead=3, arrowsize=1.2, arrowwidth=3,
    arrowcolor=colors['axes'][0], xref="x", yref="y", axref="pixel", ayref="pixel"
)
fig.add_annotation(
    x=0, y=y_max, ax=0, ay=20, showarrow=True, arrowhead=3, arrowsize=1.2, arrowwidth=3,
    arrowcolor=colors['axes'][1], xref="x", yref="y", axref="pixel", ayref="pixel"
)

filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filepath = f"{filename_base}.png"
fig.write_image(output_filepath, scale=2)

print(f"Chart saved to {output_filepath}")