import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
output_file_path = json_file_path.with_suffix(".png")

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#1f77b4',
    texttemplate='%{y}%',
    textposition='outside',
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=30, b=100, l=80, r=20),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_standoff=15,
        range=[0, 60],
        tickvals=[0, 10, 20, 30, 40, 50, 60],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=False
    ),
    shapes=[
        go.layout.Shape(type="line", xref="x", yref="paper", x0=0.5, y0=0, x1=0.5, y1=1, line=dict(color="#f0f0f0", width=1)),
        go.layout.Shape(type="line", xref="x", yref="paper", x0=1.5, y0=0, x1=1.5, y1=1, line=dict(color="#f0f0f0", width=1)),
        go.layout.Shape(type="line", xref="x", yref="paper", x0=2.5, y0=0, x1=2.5, y1=1, line=dict(color="#f0f0f0", width=1))
    ],
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper", yref="paper",
            x=0.99, y=-0.25,
            xanchor='right', yanchor='top',
            font=dict(size=12, color='#666666')
        )
    ]
)

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
)

fig.write_image(output_file_path, scale=2)

print(f"Chart saved to {output_file_path}")