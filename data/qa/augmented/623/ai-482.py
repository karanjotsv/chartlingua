import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Scatter(
        x=chart_data['categories'],
        y=series['data'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=colors[i], width=2.5),
        marker=dict(color=colors[i], size=6)
    ))

shapes = []
for i in range(len(chart_data['categories'])):
    if i % 2 != 0:
        shapes.append(go.layout.Shape(
            type="rect",
            xref="x",
            yref="paper",
            x0=i - 0.5,
            y0=0,
            x1=i + 0.5,
            y1=1,
            fillcolor="#F8F9FA",
            layer="below",
            line_width=0,
        ))

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    shapes=shapes,
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[4.5, 18.5],
        tickvals=[5, 7.5, 10, 12.5, 15, 17.5],
        gridcolor='#EAEAEA',
        zeroline=False
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        type='category',
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
        font=dict(size=13)
    ),
    margin=dict(l=80, r=40, t=40, b=150)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=-0.35,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=12)
    )

output_filename_base = json_path.stem
output_png_path = f"{output_filename_base}.png"

fig.write_image(output_png_path, scale=2)