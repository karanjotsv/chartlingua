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

output_path = json_path.with_suffix(".png")

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    textfont=dict(size=12, family="Arial")
))

annotations = []
if texts.get('source_left'):
    annotations.append(
        go.layout.Annotation(
            text=texts['source_left'],
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            align='left'
        )
    )

if texts.get('source_right'):
    annotations.append(
        go.layout.Annotation(
            text=texts['source_right'],
            showarrow=False,
            xref='paper', yref='paper',
            x=1, y=-0.15,
            xanchor='right', yanchor='top',
            align='right'
        )
    )


fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    title_text=texts.get('title'),
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    showlegend=False,
    margin=dict(l=90, r=40, t=60, b=100),
    xaxis=dict(
        tickmode='linear',
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        range=[0, 3500],
        tick0=0,
        dtick=500,
        gridcolor='#E5E5E5',
        zeroline=False
    ),
    annotations=annotations
)

fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")