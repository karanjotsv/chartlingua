import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for plotting
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data to display from top to bottom (Plotly's default is bottom-to-top)
categories.reverse()
values.reverse()

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{text:.2f}',
    hoverinfo='none',
    cliponaxis=False # Prevent text labels from being clipped
))

# Configure layout
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts['subtitle']}"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        font=dict(size=18)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[0, 16.5],
        tickmode='linear',
        tick0=0,
        dtick=2,
        showgrid=True,
        gridcolor='#D3D3D3',
        gridwidth=1
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    showlegend=False,
    margin=dict(l=100, r=50, t=80, b=80),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.95,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(size=10)
        )
    ]
)

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=11,
        color='black'
    )
)

# Generate output filename and save the image
output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")