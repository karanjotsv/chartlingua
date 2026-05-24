import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [str(v) for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=text_labels,
    textposition='outside',
    cliponaxis=False,
    marker_color=colors[0],
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

fig.update_layout(
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='lightgrey'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 10000],
        dtick=2000,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        showline=False
    ),
    margin=dict(l=90, r=40, t=40, b=100),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

output_path = json_path.with_suffix('.png')
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")