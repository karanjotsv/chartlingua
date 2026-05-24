import sys
import json
import plotly.graph_objects as go
import os

# Load data from the JSON file provided as a command-line argument
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

x_values = [d['category'] for d in chart_data]
y_values = [d['value'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    marker_color=colors[0],
    hoverinfo='none',
    textfont=dict(
        family="Arial",
        color='black'
    ),
    cliponaxis=False
))

# Build title string
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 205],
        tickvals=[0, 25, 50, 75, 100, 125, 150, 175, 200],
        gridcolor='#e9e9e9',
        showgrid=True,
        zeroline=False,
        showline=False
    ),
    margin=dict(l=90, r=30, t=50, b=80),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper", yref="paper",
            x=0.99, y=-0.18,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=10, color='#666666')
        )
    ]
)

# Generate output filename and save the image
base_filename = os.path.splitext(os.path.basename(sys.argv[1]))[0]
fig.write_image(f"{base_filename}.png", scale=2)