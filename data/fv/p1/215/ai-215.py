import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}", file=sys.stderr)
    sys.exit(1)

data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

# Data is ordered from bottom bar to top bar in JSON to match visual
categories = [d['category'] for d in data]
values = [d['value'] for d in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0] if colors else '#1f77b4')
))

# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Combine source and note for a caption
caption_parts = []
source = texts.get('source')
if source:
    caption_parts.append(f"Source: {source}")
note = texts.get('note')
if note:
    caption_parts.append(f"Note: {note}")
caption_text = "<br>".join(caption_parts)

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        tickmode='linear'
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=230, r=30, t=80, b=80),
    annotations=[dict(
        showarrow=False,
        text=caption_text,
        xref="paper",
        yref="paper",
        x=0,
        y=-0.2,
        xanchor='left',
        yanchor='top',
        align='left'
    )] if caption_text else []
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)