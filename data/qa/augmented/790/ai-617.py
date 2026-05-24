import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=[f"<b>{v}%</b>" for v in values],
    textposition='auto',
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    ),
    insidetextanchor='end'
))

fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 95],
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgray',
        griddash='dot',
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=[
        dict(
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.25,
            xanchor="right",
            yanchor="top",
            text=texts['source'],
            showarrow=False,
            align="right",
            font=dict(
                family="Arial",
                size=12,
                color="dimgray"
            )
        )
    ]
)

output_path = json_path.with_suffix('.png')
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")