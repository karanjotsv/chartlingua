import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and settings from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines+markers+text',
        line=dict(color=colors[i % len(colors)], width=2.5),
        marker=dict(color=colors[i % len(colors)], size=7),
        text=series.get('labels'),
        textposition='top center',
        textfont=dict(family="Arial", size=12, color='#333333'),
        hoverinfo='none'
    ))

# Combine title and subtitle if they exist
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    if full_title:
        full_title += "<br>"
    full_title += f"<span style='font-size: 14px;'>{subtitle_text}</span>"

# Update layout
fig.update_layout(
    title_text=full_title,
    title_x=0.05,
    title_y=0.95,
    font=dict(family="Arial", size=12),
    showlegend=False,
    plot_bgcolor='#F9F9F9',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=50, b=80),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='linear',
        tick0=2000,
        dtick=1,
        showgrid=False,
        zeroline=False,
        range=[1999.5, 2019.5]
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[7500, 16500],
        tickvals=[8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000],
        ticktext=["8 000", "9 000", "10 000", "11 000", "12 000", "13 000", "14 000", "15 000", "16 000"],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
    )
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts.get('source'),
        xref="paper", yref="paper",
        x=0.98, y=0.01,
        showarrow=False,
        xanchor='right', yanchor='bottom',
        font=dict(size=11, color='#555555')
    )

# Define output filename and save the image
output_filename = json_file_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")