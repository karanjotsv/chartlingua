import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_details.get('chart_data', {})
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=chart_data.get('labels', []),
    values=chart_data.get('values', []),
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    hole=0,
    sort=False,  # Preserve the original order of the data
    direction='clockwise',
    showlegend=True,
    textinfo='none'  # No text labels on the pie slices
))

# Combine title and source for the caption
caption_parts = []
title_text = texts.get('title')
if title_text:
    caption_parts.append(f"<b>{title_text}</b>")

source_text = texts.get('source')
if source_text:
    caption_parts.append(source_text)

caption = " ".join(caption_parts)

# Update layout for styling, fonts, and annotations
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='#D3D3D3',
    paper_bgcolor='white',
    margin=dict(l=40, r=40, t=40, b=200),  # Increased bottom margin for the caption
    legend=dict(
        x=1,
        y=1,
        xanchor='left',
        yanchor='top',
        traceorder='normal',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    ),
    annotations=[
        dict(
            text=caption,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.25,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ]
)

# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")