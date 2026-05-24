import sys
import json
import plotly.graph_objects as go
import pathlib

# Check if a command-line argument is provided
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_filepath = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_filepath.is_file():
    print(f"Error: File not found at {json_filepath}")
    sys.exit(1)

# Read the JSON data
with open(json_filepath, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and text from the JSON structure
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='outside',
    texttemplate='%{text:,.0f}',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Build the title string
title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout for a clean and accurate look
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left',
        y=0.95,
        yanchor='top',
        font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickfont=dict(family="Arial", size=12, color='black')
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        range=[0, 14000000],
        dtick=2000000,
        tickfont=dict(family="Arial", size=10, color='black')
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(t=80, b=80, l=80, r=40)
)

# Define the output filename from the input JSON path
output_filepath = json_filepath.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_filepath, scale=2)

print(f"Chart saved to {output_filepath}")