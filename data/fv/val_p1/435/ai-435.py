import sys
import os
import json
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for the chart
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    hoverinfo='label+percent+value',
    textinfo='value',
    textposition='outside',
    sort=False,
    direction='clockwise'
))

# Update layout and styling
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += title_text
    if subtitle_text:
        full_title += f"<br><sub>{subtitle_text}</sub>"

source_text = texts.get('source')

fig.update_layout(
    title_text=full_title,
    title_x=0.5,
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.7,
        xanchor="left",
        x=1.02
    ),
    margin=dict(l=60, r=200, t=60, b=60),
    paper_bgcolor='rgba(255,255,255,1)',
    plot_bgcolor='rgba(255,255,255,1)'
)

# Add source annotation if it exists
if source_text:
    fig.add_annotation(
        text=source_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.1,
        xanchor='left',
        yanchor='top'
    )

# Determine the output filename from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a high-resolution PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have 'kaleido' installed (`pip install kaleido`)")
    sys.exit(1)