import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# To match the visual order of the original chart (highest value at the top),
# we need to reverse the data lists for Plotly's bottom-to-top rendering.
reversed_data = chart_data[::-1]
categories = [item['category'] for item in reversed_data]
values = [item['value'] for item in reversed_data]

# Create the bar trace
fig = go.Figure()

fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(
        color=colors[0] if colors else '#3385c9',
        line=dict(width=0)
    ),
    text=values,
    textposition='outside',
    texttemplate='%{text:,}',
    cliponaxis=False  # Allow text to be drawn outside the plot area
))

# Combine title and subtitle
title_text_parts = []
if texts.get("title"):
    title_text_parts.append(f"<b>{texts['title']}</b>")
if texts.get("subtitle"):
    title_text_parts.append(f"<span style='font-size: 14px;'>{texts['subtitle']}</span>")
title_text = "<br>".join(title_text_parts)

# Combine source and note for annotation
source_text_parts = []
if texts.get("source"):
    source_text_parts.append(texts["source"])
if texts.get("note"):
    source_text_parts.append(texts["note"])
source_note_text = "<br>".join(source_text_parts)

# Update layout for a professional look and feel
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e5e5e5',
        zeroline=False,
        showline=False,
        ticks='outside',
        tickformat=',',
        dtick=5000,
        range=[0, max(values) * 1.15] # Ensure space for text labels
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        autorange='reversed'
    ),
    margin=dict(l=150, r=60, t=40, b=80),
    showlegend=False,
    annotations=[
        dict(
            text=source_note_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.12,  # Position below x-axis title
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color="#666666")
        )
    ]
)

# Generate the output filename from the input JSON path
output_filename = json_path.with_suffix('.png').name

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")