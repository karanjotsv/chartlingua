import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts from the JSON structure
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
    marker=dict(
        color=colors[0],
        line=dict(
            color='black',
            width=1.5
        )
    ),
    text=values,
    textposition='auto',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    hoverinfo='none' # Hides hover labels as they are not in the original
))

# Combine title and subtitle if available
title_text = texts['title']
if texts['subtitle']:
    title_text += f"<br><sup>{texts['subtitle']}</sup>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=14)
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=False,
        showticklabels=False, # Y-axis labels are not visible in the original
        range=[0, max(values) * 1.15] # Add padding for text on top
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(t=100, b=50, l=50, r=50) # Adjust top margin for the long title
)

# Set up the source/note as an annotation if it exists
if texts['source']:
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.15, # Position below the x-axis
        xanchor='left',
        yanchor='top'
    )

# Define the output filename based on the input JSON file's name
output_filename = json_file_path.stem + '.png'

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")