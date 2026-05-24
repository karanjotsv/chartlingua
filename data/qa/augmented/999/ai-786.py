import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
base_filename = Path(json_file_path).stem

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data for top-to-bottom display in Plotly horizontal bar chart
categories.reverse()
values.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    texttemplate='%{x}',
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial")
))

title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>" if full_title else f"<sub>{subtitle_text}</sub>"

source_text = texts.get('source')
note_text = texts.get('note')
caption_text = ""
if source_text:
    caption_text += source_text
if note_text:
    caption_text += f"<br><i>{note_text}</i>" if caption_text else f"<i>{note_text}</i>"

fig.update_layout(
    title=dict(
        text=full_title if full_title else None,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        range=[0, max(values) * 1.15],
        tick0=0,
        dtick=50
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    margin=dict(l=360, r=40, t=50, b=80)
)

if caption_text:
    fig.add_annotation(
        text=caption_text,
        xref="paper", yref="paper",
        x=1, y=-0.15,
        xanchor='right', yanchor='top',
        align='right',
        showarrow=False,
        font=dict(size=10)
    )

output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")