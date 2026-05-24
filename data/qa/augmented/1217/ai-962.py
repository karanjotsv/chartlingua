import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data for plotting
data_series = chart_data['chart_data']
categories = [item['category'] for item in data_series]
values = [item['value'] for item in data_series]

texts = chart_data['texts']
colors = chart_data['colors']

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Combine title and subtitle if they exist
title_text = ""
if texts['title']:
    title_text += texts['title']
if texts['subtitle']:
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Combine source and note for the annotation
source_text = ""
if texts['source']:
    source_text += texts['source']
if texts['note']:
    # Add a line break if both source and note exist
    if texts['source']:
        source_text += "<br>"
    source_text += texts['note']

# Update layout
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    title_text=title_text,
    title_x=0.05,
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 250],
        tickvals=[0, 50, 100, 150, 200, 250],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        title_font=dict(size=14),
        tickfont=dict(size=12)
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.25, # Adjusted for bottom margin
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Determine output filename from input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")