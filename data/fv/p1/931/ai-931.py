import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: {Path(sys.argv[0]).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,
    direction='clockwise',
    rotation=-80,
    domain=dict(x=[0, 0.65])
))

title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    title_y=0.95,
    title_xanchor='left',
    title_yanchor='top',
    title_font=dict(size=20, family="Arial"),
    font=dict(family="Arial", size=14),
    legend=dict(
        x=0.68,
        y=0.9,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(0,0,0,0)',
        traceorder='normal'
    ),
    margin=dict(l=20, r=20, t=100, b=40),
    showlegend=True,
    paper_bgcolor='white',
    plot_bgcolor='white'
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.01,
        y=-0.08,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=12)
    )

output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2, width=900, height=550)

print(f"Chart saved to {output_filename}")