import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts from JSON
chart_data = chart_json.get('chart_data', [])
texts = chart_json.get('texts', {})
colors = chart_json.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#297ACC',
    text=values,
    texttemplate='%{y:.1f}%',
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Construct title and source strings
title_text = texts.get('title')
if title_text and texts.get('subtitle'):
    title_text = f"<b>{title_text}</b><br><sub>{texts.get('subtitle')}</sub>"
elif title_text:
    title_text = f"<b>{title_text}</b>"

source_text = texts.get('source', '')
if texts.get('note'):
    source_text += f"<br>{texts.get('note')}"

# Update layout
fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    title_font_family="Arial",
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=60, b=80),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black'
    ),
    yaxis=dict(
        range=[0, 50],
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    )
)

# Add source annotation
if source_text:
    fig.add_annotation(
        text=source_text,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        font=dict(
            family="Arial",
            size=10,
            color='#666666'
        )
    )

# Generate output filename from JSON path
output_filename = f"{pathlib.Path(json_path).stem}.png"

# Save the figure as a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as '{output_filename}'")