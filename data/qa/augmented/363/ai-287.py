import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Load data from the JSON file provided as a command-line argument
json_path = Path(sys.argv[1])
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data and texts for plotting
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the bar chart trace
fig = go.Figure(
    data=[go.Bar(
        x=categories,
        y=values,
        marker_color=colors[0],
        text=values,
        textposition='outside',
        textfont=dict(size=12),
        cliponaxis=False
    )]
)

# Combine title and subtitle, handling null values
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts['subtitle']}"
if not title_text:
    title_text = None

# Create annotations for the source text
annotations = []
if texts.get('source'):
    annotations.append(dict(
        text=texts['source'],
        xref="paper", yref="paper",
        x=1, y=-0.15,
        xanchor='right', yanchor='top',
        showarrow=False,
        font=dict(size=12)
    ))

# Update layout with styling to match the original image
fig.update_layout(
    title=dict(text=title_text),
    xaxis_title_text=texts.get('xaxis_title'),
    yaxis_title_text=texts.get('yaxis_title'),
    yaxis_range=[0, 25],
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False
    ),
    font=dict(family="Arial"),
    margin=dict(t=50, b=80, l=90, r=40),
    annotations=annotations,
    showlegend=False
)

# Generate the output PNG file
output_path = json_path.with_suffix(".png")
fig.write_image(str(output_path), scale=2)
print(f"Chart saved to {output_path}")