import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

# The JSON file is the sole source of data, text, and styling.
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_image_path = json_path.with_suffix('.png')

# Load all chart information from the JSON file, ensuring UTF-8 encoding for multilingual support.
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', {})

# Extract data for the pie chart, preserving the order from the JSON file.
labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the pie chart trace.
# The 'sort=False' argument is critical to maintain the original data order.
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors.get('slices')),
    textinfo='percent',
    texttemplate='%{value:.1f}%',
    hoverinfo='label+percent',
    sort=False,
    textposition='outside'
)

fig = go.Figure(data=[pie_trace])

# Combine title and subtitle using HTML for rich text formatting.
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Apply layout settings, meticulously positioning elements and setting fonts.
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(
            family='Arial',
            size=24,
            color=colors.get('title_font')
        )
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.15,
        xanchor='center',
        x=0.5
    ),
    paper_bgcolor=colors.get('background'),
    plot_bgcolor=colors.get('background'),
    font=dict(
        family="Arial",
        size=12,
        color=colors.get('text_font')
    ),
    # Set margins to prevent title, labels, or legend from being clipped.
    margin=dict(t=100, b=100, l=40, r=40)
)

# Specifically style the outside text labels for better visibility.
fig.update_traces(
    outsidetextfont=dict(
        size=14,
        color=colors.get('text_font')
    )
)

# Generate the final chart as a high-resolution PNG image.
fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to '{output_image_path}'")