import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get file path from argument
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

# Extract data for plotting
chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

# Create figure
fig = go.Figure()

# Add traces based on series data
categories = chart_data['categories']
for i, series in enumerate(chart_data['series']):
    if series['type'] == 'bar':
        fig.add_trace(go.Bar(
            x=categories,
            y=series['y'],
            name=series['name'],
            yaxis=series.get('yaxis', 'y1'),
            marker_color=colors[i],
            marker_line=dict(color='black', width=1)
        ))
    elif series['type'] == 'scatter':
        fig.add_trace(go.Scatter(
            x=categories,
            y=series['y'],
            name=series['name'],
            mode='markers',
            yaxis=series.get('yaxis', 'y2'),
            marker=dict(
                color=colors[i],
                symbol='diamond-tall',
                size=7
            )
        ))

# Build title and source strings
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

source_text = texts.get('source')
note_text = texts.get('note')
source_note_text = ""
if source_text:
    source_note_text += f"Source: {source_text}"
if note_text:
    source_note_text += f"<br>{note_text}"

# Update layout
fig.update_layout(
    font=dict(family="Arial"),
    title=dict(text=full_title, x=0.05, xanchor='left'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        type='category',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 70],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside',
        gridcolor='#CCCCCC' # Faint gridlines as in original
    ),
    yaxis2=dict(
        title=texts.get('y2_axis_title'),
        overlaying='y',
        side='right',
        range=[0, 70],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside',
        showgrid=False
    ),
    margin=dict(l=80, r=80, t=80, b=80),
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2, # Adjust this value to position the source/note text
            xanchor='left',
            yanchor='top',
            text=source_note_text,
            showarrow=False,
            align='left'
        )
    ]
)

# Generate output image file
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")