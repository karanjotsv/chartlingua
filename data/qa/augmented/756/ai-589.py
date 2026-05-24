import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}", file=sys.stderr)
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        marker_color=colors[i % len(colors)],
        text=series['y'],
        textposition='outside',
        cliponaxis=False,
        textfont=dict(family="Arial", size=12, color='black'),
        showlegend=False
    ))

title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

annotations = []
if texts.get('note'):
    annotations.append(
        go.layout.Annotation(
            xref="paper", yref="paper",
            x=0, y=-0.12,
            xanchor="left", yanchor="top",
            text=texts['note'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#0000ff")
        )
    )
if texts.get('source'):
    annotations.append(
        go.layout.Annotation(
            xref="paper", yref="paper",
            x=1, y=-0.12,
            xanchor="right", yanchor="top",
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="gray")
        )
    )

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        xanchor='left'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 600],
        tickvals=[0, 100, 200, 300, 400, 500, 600],
        gridcolor='lightgray'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linecolor='lightgray'
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=50, b=100),
    annotations=annotations
)

output_path = json_path.with_suffix(".png")
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")