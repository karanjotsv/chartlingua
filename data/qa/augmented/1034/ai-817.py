import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# The script must accept the JSON path as a required command-line argument.
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read the JSON file, which is the sole source of data and text.
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the JSON structure.
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly, preserving the original order.
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Initialize the figure.
fig = go.Figure()

# Add the bar trace.
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=values,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Prevent text on bars from being clipped
))

# Handle title and subtitle creation.
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
final_title = ""
if title_text:
    final_title += f"<b>{title_text}</b>"
if subtitle_text:
    final_title += f"<br><i>{subtitle_text}</i>" if final_title else f"<i>{subtitle_text}</i>"

# Update layout to match the original chart's appearance and address potential issues.
fig.update_layout(
    title_text=final_title if final_title else None,
    title_x=0.05,
    xaxis_title_text=texts.get('x_axis_title'),
    yaxis_title_text=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12),
    yaxis=dict(
        range=[0, 400],
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    xaxis=dict(
        type='category',
        showgrid=False
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100) # Adjust margins to prevent clipping
)

# Add source text as an annotation for precise positioning.
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=1, y=-0.22,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(family="Arial", size=10, color="grey")
    )

# Derive the output filename from the input JSON path.
output_filename = json_path.with_suffix('.png')

# Save the chart as a high-resolution PNG image.
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")