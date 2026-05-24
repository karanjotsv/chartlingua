import sys
import json
import plotly.graph_objects as go
import os

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
# The data is ordered from highest to lowest, which means it needs to be reversed
# for Plotly's horizontal bar chart to display correctly (highest at the top).
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

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
    texttemplate='%{text}',
    cliponaxis=False,
    hoverinfo='y+x'
))

# Combine title and subtitle
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += title_text
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

# Combine source and note for annotation
source_text = texts.get('source_text', '')
note_text = texts.get('note_text', '')
source_note_text = ""
if source_text:
    source_note_text += source_text
if note_text:
    source_note_text += f"<br>{note_text}"

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(
        text=full_title,
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        showline=False,
        ticks='outside',
        tickcolor='grey'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        categoryorder='array', 
        categoryarray=categories
    ),
    margin=dict(l=120, r=60, t=60, b=80),
    showlegend=False,
    annotations=[
        dict(
            showarrow=False,
            text=source_note_text,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.15,
            xanchor="left",
            yanchor="top",
            align="left",
            font=dict(size=10, color="grey")
        )
    ]
)

# Set format for the text on bars
fig.update_traces(textfont_size=12, textangle=0)

# Derive output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved as {output_image_path}")