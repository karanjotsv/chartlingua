import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

fig = go.Figure()

chart_data = chart_info['chart_data']
colors = chart_info['colors']
texts = chart_info['texts']

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=colors[i], width=3),
        marker=dict(color=colors[i], size=8)
    ))

if texts.get('annotations'):
    for ann in texts['annotations']:
        fig.add_annotation(
            x=ann.get('x'),
            y=ann.get('y'),
            text=ann.get('text'),
            showarrow=False,
            font=dict(family="Arial", size=12, color="#CCCCCC"),
            xanchor=ann.get('xanchor', 'center'),
            yanchor=ann.get('yanchor', 'middle'),
            xshift=ann.get('xshift', 0),
            yshift=ann.get('yshift', 0)
        )

fig.update_layout(
    title=dict(
        text=texts.get('title'),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=24)
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=14, color="#FFFFFF"),
    plot_bgcolor='#0c243f',
    paper_bgcolor='#0c243f',
    xaxis=dict(
        range=[2009.5, 2028.5],
        tickmode='linear',
        tick0=2010,
        dtick=2,
        gridcolor='#666666',
        linecolor='#FFFFFF'
    ),
    yaxis=dict(
        range=[-150, 3150],
        tickmode='linear',
        tick0=0,
        dtick=500,
        gridcolor='#666666',
        linecolor='#FFFFFF'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.35,
        xanchor="center",
        x=0.5,
        font=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=100, b=120)
)

output_path = f"{json_path.stem}.png"
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")