import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data for plotting
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('name', ''),
        line=dict(color=colors[i] if i < len(colors) else None, width=2.5)
    ))

# Construct title and subtitle string
title_text = texts.get('title', '')
subtitle_text = texts.get('subtitle', '')
if title_text and subtitle_text:
    full_title = f"{title_text}<br><sub>{subtitle_text}</sub>"
else:
    full_title = title_text or subtitle_text or ''

# Construct source and note string
source_text = texts.get('source', '')
note_text = texts.get('note', '')
if source_text and note_text:
    caption_text = f"Source: {source_text}<br>Note: {note_text}"
elif source_text:
    caption_text = f"Source: {source_text}"
elif note_text:
    caption_text = f"Note: {note_text}"
else:
    caption_text = ""

# Update layout
fig.update_layout(
    title=dict(
        text=full_title,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title', ''),
        tickmode='array',
        tickvals=list(range(12)),
        range=[-0.2, 11],
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title=texts.get('y_axis_title', ''),
        type='log',
        tickmode='array',
        tickvals=[1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048],
        range=[0, 3.31], # Corresponds to 10^0 to 10^3.31, which is 1 to 2048
        showgrid=True,
        gridcolor='#D3D3D3'
    ),
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=False,
    margin=dict(l=60, r=30, t=60, b=60)
)

# Add source/note caption if it exists
if caption_text:
    fig.add_annotation(
        text=caption_text,
        xref="paper", yref="paper",
        x=0, y=-0.15,
        showarrow=False,
        align="left",
        xanchor="left",
        yanchor="top"
    )

# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")