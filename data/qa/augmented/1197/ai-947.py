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

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
bar_texts = [f"{v}%" for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=bar_texts,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

# --- Configure Layout ---

# Combine title and subtitle
title_text = texts.get('title', '') or ''
subtitle_text = texts.get('subtitle', '') or ''
if subtitle_text:
    title_text = f"{title_text}<br><sub>{subtitle_text}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[0, max(values) * 1.2], # Proactive range setting
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',  # To display the highest value at the top
        showgrid=False
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=110, r=50, t=50, b=80), # Margins to prevent clipping
    showlegend=False
)

# Add source annotation
source_text = texts.get('source', '')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0.99, y=-0.15,  # Positioned at the bottom right
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=10, color='gray')
    )

# --- Output ---

# Define the output image filename based on the input JSON filename
output_filename = json_file_path.with_suffix('.png').name

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")