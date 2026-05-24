import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
pull_data = config.get('pull', [0] * len(chart_data))

values = [d['value'] for d in chart_data]
labels = [d['category'] for d in chart_data]
custom_text = [f"{d['category']}, {d['value']}<br>{d['percentage']}%" for d in chart_data]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    text=custom_text,
    textposition='outside',
    textinfo='text',
    hoverinfo='label+percent+value',
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    pull=pull_data,
    sort=False,
    direction='clockwise'
)])

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts['subtitle']}"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    margin=dict(l=100, r=100, t=100, b=50)
)

source_note_text = []
if texts.get('source'):
    source_note_text.append(texts['source'])
if texts.get('note'):
    source_note_text.append(texts['note'])

if source_note_text:
    fig.add_annotation(
        text="<br>".join(source_note_text),
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.1,
        xanchor='left',
        yanchor='top'
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}", file=sys.stderr)
    sys.exit(1)