import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and text from the configuration
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the main line trace
fig.add_trace(go.Scatter(
    x=categories,
    y=values,
    mode='lines+markers+text',
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=7),
    text=values,
    textposition='top center',
    textfont=dict(family="Arial", size=11, color='#000000'),
    hoverinfo='none',
    showlegend=False
))

# Build title and source strings, handling null values
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_parts = []
if texts.get('note'):
    source_parts.append(f"<i>{texts['note']}</i>")
if texts.get('source'):
    source_parts.append(texts['source'])
source_text = "<br>".join(source_parts)

# Update layout for a professional look and feel
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='outside',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        ticks='outside',
        tickfont=dict(size=12),
        range=[400, 475] # Set range to give space for labels
    ),
    margin=dict(l=80, r=40, t=60, b=100),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=11)
        )
    ]
)

# Define output filename and save the image
output_filename = json_file_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")