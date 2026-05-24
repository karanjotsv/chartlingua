import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
    sort=False,
    direction='clockwise',
    textinfo='none',
    hoverinfo='label+percent'
))

title_parts = []
if texts.get('title'):
    title_parts.append(texts['title'])
if texts.get('subtitle'):
    title_parts.append(f"<br><sub>{texts['subtitle']}</sub>")
title_text = "".join(title_parts)

source_note_parts = []
if texts.get('source'):
    source_note_parts.append(texts['source'])
if texts.get('note'):
    source_note_parts.append(texts['note'])
source_note_text = "<br>".join(source_note_parts)

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        y=0.95,
        yanchor='top'
    ),
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.01
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=50, r=500, t=100, b=80),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=[
        dict(
            showarrow=False,
            text=source_note_text,
            x=0,
            y=-0.1,
            xref="paper",
            yref="paper",
            xanchor="left",
            yanchor="top",
            align="left"
        )
    ] if source_note_text else []
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")