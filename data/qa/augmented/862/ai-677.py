import sys
import json
import plotly.graph_objects as go
import pathlib

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_filepath = sys.argv[1]

# Read the JSON data file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_filepath}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_filepath}'")
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0] if colors else '#1f77b4',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    cliponaxis=False
))

# Build combined title and source strings
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br>{subtitle_text}"

source_text = texts.get('source')
note_text = texts.get('note')
caption_text = []
if source_text:
    caption_text.append(source_text)
if note_text:
    caption_text.append(note_text)
full_caption = "<br>".join(caption_text)

# Update layout for a clean, professional look
fig.update_layout(
    font=dict(family="Arial"),
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 17.5],
        tickvals=[0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5],
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        linecolor='black'
    ),
    showlegend=False,
    margin=dict(l=90, r=30, t=50, b=120),
    annotations=[
        dict(
            showarrow=False,
            text=full_caption,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.25, # Position below x-axis
            xanchor='right',
            yanchor='top',
            align='right'
        )
    ]
)

# Derive output filename from the input JSON filename
output_filename = f"{pathlib.Path(json_filepath).stem}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")