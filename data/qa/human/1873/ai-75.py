import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get file path from command-line argument
json_file_path = pathlib.Path(sys.argv[1])
output_image_path = json_file_path.with_suffix(".png")

# Load data from JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading JSON file: {e}")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = chart_config.get("chart_data", [])
texts = chart_config.get("texts", {})
colors = chart_config.get("colors", [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    texttemplate='%{label} %{value}%',
    textposition='outside',
    hoverinfo='none',
    sort=False,
    direction='clockwise'
))

# Build title and source annotations
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
source_text = texts.get('source')
note_text = texts.get('note')

full_title = ""
if title_text:
    full_title = f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br>{subtitle_text}"

annotations = []
if source_text or note_text:
    footer_elements = []
    if note_text:
        footer_elements.append(note_text)
    if source_text:
        footer_elements.append(source_text)
    
    annotations.append(go.layout.Annotation(
        text="<br>".join(footer_elements),
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=0,
        xanchor='right',
        yanchor='top',
        yshift=-10  # Shift down to avoid overlap with chart
    ))

# Update layout
fig.update_layout(
    title_text=full_title,
    title_x=0.05,
    title_y=0.95,
    title_xanchor='left',
    title_yanchor='top',
    showlegend=False,
    font=dict(family="Arial", size=14, color="black"),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=100, r=100, t=60, b=80),
    annotations=annotations
)

# Write the image to a file
fig.write_image(str(output_image_path), scale=2)

print(f"Chart saved to {output_image_path}")