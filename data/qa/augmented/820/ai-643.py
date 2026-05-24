import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data from the JSON object
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Create the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None
    ))

# Build combined title string
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br>{texts['subtitle']}"

# Prepare annotations for source and note
annotations = []
source_note_text = []
if texts.get("source"):
    source_note_text.append(texts["source"])
if texts.get("note"):
    source_note_text.append(texts["note"])

if source_note_text:
    annotations.append(
        dict(
            text="<br>".join(source_note_text),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    )

# Update layout
fig.update_layout(
    title_text=title_text if title_text else None,
    font=dict(family="Arial"),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        linecolor='lightgrey'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 700000],
        gridcolor='lightgrey'
    ),
    plot_bgcolor='white',
    paper_bgcolor='#f0f2f5',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=annotations
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")