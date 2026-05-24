import sys
import json
import os
import plotly.graph_objects as go

# Ensure the script is called with a single argument: the path to the JSON file.
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the JSON file exists before proceeding.
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Load the chart data and configuration from the specified JSON file.
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded JSON object.
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly by separating categories and values.
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize the figure.
fig = go.Figure()

# Add the horizontal bar trace to the figure.
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{x:.2f}',
    cliponaxis=False  # Prevent text labels from being clipped by the plot area.
))

# Combine title and subtitle using HTML for rich formatting.
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if subtitle_text:
    title_text = f"<b>{title_text}</b><br><sub>{subtitle_text}</sub>"

# Configure the layout of the chart to match the original image.
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[0, 4.5],
        showgrid=True,
        gridcolor='#E0E0E0',
        zeroline=False,
        showline=False,
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',  # Display data from top to bottom as in the original.
        showgrid=False,
        zeroline=False,
        showline=False,
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    showlegend=False,
    margin=dict(l=220, r=50, t=40, b=80),  # Adjust margins to prevent label clipping.
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='#666666')
        )
    ]
)

# Determine the output filename from the input JSON file path.
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image.
fig.write_image(output_image_path, scale=2)

print(f"Chart saved successfully to {output_image_path}")