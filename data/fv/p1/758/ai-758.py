import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    showlegend=False,
    hoverinfo='none',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        font=dict(
            family="Arial",
            size=16
        )
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        showline=False,
        range=[0, max(values) * 1.15]
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    margin=dict(l=40, r=40, t=80, b=100),
    shapes=[
        dict(
            type='rect',
            xref='paper',
            yref='paper',
            x0=0,
            y0=0,
            x1=1,
            y1=1,
            line=dict(
                color='black',
                width=1
            )
        )
    ]
)

output_path = json_path.with_suffix('.png')
fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")