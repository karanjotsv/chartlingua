import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts
data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
annotations_data = chart_data.get('annotations', [])

# Create figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i]
    ))

# Build combined title and source/note strings
title_text = f"<b>{texts['title']}</b>" if texts.get('title') else ""
if texts.get('subtitle'):
    title_text += f"<br>{texts['subtitle']}"

source_note_text = ""
if texts.get('source'):
    source_note_text += texts['source']
if texts.get('note'):
    source_note_text += f"<br>{texts['note']}"

# Add annotations for total values on top of bars
for ann in annotations_data:
    fig.add_annotation(
        x=ann['x'],
        y=ann['y'],
        text=ann['text'],
        showarrow=False,
        font=dict(
            family="Arial",
            size=10,
            color="#333333"
        ),
        yshift=5
    )

# Add source and note annotation at the bottom
if source_note_text:
    fig.add_annotation(
        text=source_note_text,
        xref="paper", yref="paper",
        x=0, y=-0.25,
        showarrow=False,
        align="left",
        font=dict(family="Arial", size=12, color="grey")
    )

# Update layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickangle=-45,
        type='category'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1600],
        tickmode='linear',
        dtick=50,
        showgrid=True,
        gridwidth=1,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False
    ),
    yaxis2=dict(
        range=[0, 1600],
        tickmode='linear',
        dtick=50,
        overlaying='y',
        side='right',
        showgrid=False,
        zeroline=False
    ),
    font=dict(
        family="Arial"
    ),
    showlegend=False,
    plot_bgcolor='white',
    margin=dict(l=60, r=60, t=80, b=150),
    autosize=False,
    width=1000,
    height=600
)

# Define output filename and save the image
output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")