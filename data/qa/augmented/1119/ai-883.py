import sys
import json
import os
import plotly.graph_objects as go

# Read the JSON file path from the first command-line argument
json_path = sys.argv[1]

# Load chart data and settings from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Initialize the figure object
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0]
))

# Build title and subtitle string using HTML tags
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Configure the chart layout to match the original image
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        type='category',
        showgrid=False,
        showline=True,
        linecolor='lightgray'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 12.5],
        tickvals=[0, 2.5, 5, 7.5, 10, 12.5],
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=False
    ),
    margin=dict(l=80, r=40, t=50, b=120),
    title_text=title_text if title_text else None,
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=-0.22,
            xanchor='right', yanchor='top',
            align='right'
        )
    ]
)

# Determine the output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_file = f"{base_name}.png"

# Save the chart as a high-resolution PNG image
fig.write_image(output_file, scale=2)

print(f"Chart saved to {output_file}")