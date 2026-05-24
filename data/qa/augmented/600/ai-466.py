import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}", file=sys.stderr)
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data][::-1]
values = [item['value'] for item in chart_data][::-1]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{x}',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = ""
if texts.get('source'):
    source_text = texts['source']
if texts.get('note'):
    if source_text:
        source_text += "<br>"
    source_text += texts['note']

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        range=[0, 185],
        dtick=20,
        showline=False
    ),
    yaxis=dict(
        title=texts.get('y_axis_title', None),
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        tickfont=dict(size=12)
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=150, r=50, t=50, b=80),
    showlegend=False,
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper", yref="paper",
            x=1.0, y=-0.15,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=10, color="#555555")
        )
    ]
)

output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")