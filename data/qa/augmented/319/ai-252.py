import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Define the output image path from the JSON file path
output_image_path = json_file_path.with_suffix('.png')

# Load data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and text from the JSON object
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for plotting
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=values,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Build title string
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    title_text=title_text if title_text else None,
    yaxis_title=texts.get("y_axis_title"),
    xaxis_title=texts.get("x_axis_title"),
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        showline=False,
        range=[0, 125],
        tickvals=[0, 20, 40, 60, 80, 100, 120]
    ),
    xaxis=dict(
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.25,
            xanchor='right',
            yanchor='bottom',
            text=texts.get("source"),
            showarrow=False,
            align='right',
            font=dict(
                family="Arial",
                size=12,
                color="#666666"
            )
        )
    ]
)

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")