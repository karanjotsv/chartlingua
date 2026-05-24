import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_path = json_path.with_suffix(".png")

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='black', width=1.5)),
    sort=False,
    direction='clockwise',
    rotation=150,
    textinfo='none',
    hoverinfo='label+percent',
    showlegend=False
))

title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br>{subtitle_text}"

source_text = texts.get('source')
note_text = texts.get('note')
source_note_text = ""
if source_text:
    source_note_text += f"Source: {source_text}"
if note_text:
    if source_text:
        source_note_text += "<br>"
    source_note_text += f"Note: {note_text}"

fig.update_layout(
    title_text=full_title if full_title else None,
    title_x=0.5,
    title_y=0.95,
    title_xanchor='center',
    title_yanchor='top',
    paper_bgcolor='#000000',
    plot_bgcolor='#000000',
    font=dict(family="Arial", size=12, color="white"),
    margin=dict(t=50, b=50, l=50, r=50),
    showlegend=False
)

if source_note_text:
    fig.add_annotation(
        text=source_note_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=0,
        xanchor='left',
        yanchor='bottom',
        font=dict(size=10)
    )

fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")