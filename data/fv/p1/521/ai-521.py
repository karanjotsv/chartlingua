import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Extract categories and pivot data for Plotly
categories = [item['category'] for item in chart_data]
num_series = len(texts['legend_labels'])
series_data = [[item['values'][i] for item in chart_data] for i in range(num_series)]

# Reverse data to match top-to-bottom order of the original image
categories.reverse()
for s_data in series_data:
    s_data.reverse()

fig = go.Figure()

for i in range(num_series):
    fig.add_trace(go.Bar(
        y=categories,
        x=series_data[i],
        name=texts['legend_labels'][i],
        orientation='h',
        marker=dict(color=colors[i])
    ))

# Combine title and subtitle
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += title_text
    if subtitle_text:
        full_title += f"<br><sub>{subtitle_text}</sub>"

# Combine source and note for an annotation
source_text = texts.get('source', '')
note_text = texts.get('note', '')
caption_parts = []
if source_text:
    caption_parts.append(source_text)
if note_text:
    caption_parts.append(note_text)
caption_text = "<br>".join(caption_parts)

annotations = []
if caption_text:
    annotations.append(dict(
        text=caption_text,
        showarrow=False,
        xref='paper', yref='paper',
        x=0, y=-0.25,  # Adjusted to be below the legend
        xanchor='left', yanchor='top',
        align='left'
    ))

fig.update_layout(
    barmode='group',
    title=dict(
        text=full_title if full_title else None,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
        title_text=texts.get('legend_title')
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=300, r=30, t=50, b=100),
    annotations=annotations
)

# Derive output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")