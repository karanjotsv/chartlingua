import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}", file=sys.stderr)
    sys.exit(1)

output_path = json_path.with_suffix('.png')

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

values = [d['value'] for d in chart_data]
labels_for_template = [d['label'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    values=values,
    customdata=labels_for_template,
    texttemplate="%{customdata}<br>%{value}%",
    textposition='inside',
    marker_colors=colors,
    sort=False,
    direction='clockwise',
    rotation=92,
    insidetextfont=dict(family="Arial", size=14, color='black'),
    hole=0
))

title_text = texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = ""
if texts.get('source'):
    source_text = texts['source']
if texts.get('note'):
    if source_text:
        source_text += f"<br>{texts['note']}"
    else:
        source_text = texts['note']

fig.update_layout(
    title=dict(
        text=title_text,
        font=dict(family="Arial", size=16),
        x=0.01,
        xanchor='left'
    ),
    showlegend=False,
    font=dict(family="Arial", size=12),
    margin=dict(t=120, b=100, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=0.1,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(family="Arial", size=12)
        )
    ],
    shapes=[
        dict(
            type='line',
            xref='paper',
            yref='paper',
            x0=0,
            y0=0.15,
            x1=1,
            y1=0.15,
            line=dict(
                color='black',
                width=0.5
            )
        )
    ]
)

fig.write_image(str(output_path), scale=2)
print(f"Chart saved to {output_path}")