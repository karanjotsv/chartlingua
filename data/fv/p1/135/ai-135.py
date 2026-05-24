import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
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

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    showlegend=False
))

title_text = texts.get('title', '')
subtitle_text = texts.get('subtitle')
if subtitle_text:
    title_text = f"{title_text}<br><sub>{subtitle_text}</sub>"

source_text = texts.get('source')
note_text = texts.get('note')
caption_parts = []
if source_text:
    caption_parts.append(f"Source: {source_text}")
if note_text:
    caption_parts.append(f"Note: {note_text}")
caption_text = "<br>".join(caption_parts)

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20}
    },
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False,
        categoryorder='array',
        categoryarray=categories
    ),
    yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=True,
        gridcolor='darkgray',
        range=[0, 3.5],
        dtick=0.5
    ),
    margin=dict(l=90, r=30, t=90, b=80),
    bargap=0.15
)

if caption_text:
    fig.add_annotation(
        text=caption_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.20,
        xanchor='left',
        yanchor='top'
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)