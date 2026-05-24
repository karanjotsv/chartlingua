import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = data.get('chart_data', [])
texts = data.get('texts', {})
colors = data.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
pulls = [item.get('pull', 0) for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    pull=pulls,
    marker_colors=colors,
    textinfo='none',
    textposition='auto',
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
))

title_parts = []
if texts.get('title'):
    title_parts.append(f"<b>{texts['title']}</b>")
if texts.get('subtitle'):
    title_parts.append(f"<br>{texts['subtitle']}")

source_parts = []
if texts.get('source'):
    source_parts.append(texts['source'])
if texts.get('note'):
    source_parts.append(texts['note'])

if source_parts:
    source_text = "<br>".join(source_parts)
    title_parts.append(f"<br><sub>{source_text}</sub>")

full_title = "".join(title_parts)

fig.update_layout(
    title_text=full_title,
    title_x=0.5,
    title_xanchor='center',
    showlegend=False,
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=80, r=80, t=80, b=80),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")