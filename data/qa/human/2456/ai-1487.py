import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get file path from command-line argument
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data_json = json.load(f)

# Extract data, texts, and colors from JSON
chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', [])

# Prepare data for Plotly pie chart
labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create formatted labels for the legend to include values, matching the original's style
formatted_labels_with_values = [f"{d['label']} {d['value']}%" for d in chart_data]

# Create the pie chart trace
fig = go.Figure(data=[go.Pie(
    labels=formatted_labels_with_values,
    values=values,
    marker_colors=colors,
    hoverinfo='label+percent',
    textinfo='none',
    sort=False, # Preserve the order from the JSON file
    direction='clockwise'
)])

# Combine title and subtitle
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if title_text and subtitle_text:
    full_title = f"{title_text}<br><sub>{subtitle_text}</sub>"
else:
    full_title = title_text or subtitle_text

# Update layout
fig.update_layout(
    title_text=full_title,
    title_x=0.5,
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=True,
    legend=dict(
        x=1.05,
        y=0.5,
        xanchor='left',
        yanchor='middle'
    ),
    margin=dict(l=40, r=200, t=60, b=80), # Add right margin for legend
    annotations=[
        dict(
            text=texts.get('source', ''),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=0.01,
            xanchor='right',
            yanchor='bottom'
        )
    ]
)

# Define output filename and save the image
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")