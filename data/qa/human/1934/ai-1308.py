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

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except Exception as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [item['label'] for item in data]
values = [item['value'] for item in data]
custom_text = [f"{item['label']} {item['value']}%" for item in data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
    text=custom_text,
    textinfo='text',
    textposition='outside',
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text = f"<b>{title_text}</b><br>{texts.get('subtitle')}" if title_text else texts.get('subtitle')

source_parts = []
if texts.get('source'):
    source_parts.append(texts['source'])
if texts.get('note'):
    source_parts.append(texts['note'])
source_text = "<br>".join(source_parts)

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(family="Arial"),
    showlegend=False,
    margin=dict(l=80, r=80, t=80, b=80),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.1,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ]
)

fig.update_traces(textfont_size=12)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)