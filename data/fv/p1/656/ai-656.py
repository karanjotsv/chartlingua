import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get file path from argument
json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

# Extract data from the JSON structure
chart_data = chart_spec.get('chart_data', [])
texts = chart_spec.get('texts', {})
colors = chart_spec.get('colors', [])

# Prepare data for Plotly
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    name='' # Hide trace name from hover/legend
))

# --- Layout Configuration ---

# Combine title and subtitle
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sup>{subtitle_text}</sup>"

# Combine source and note for annotations
source_text = texts.get('source')
note_text = texts.get('note')
caption_text = ""
if source_text:
    caption_text += f"Source: {source_text}"
if note_text:
    if source_text:
        caption_text += "<br>"
    caption_text += f"Note: {note_text}"

# Update layout
fig.update_layout(
    font_family="Arial",
    title_text=full_title,
    title_x=0.05,
    title_font_size=20,
    plot_bgcolor='white',
    showlegend=False,
    bargap=0.2,
    margin=dict(l=90, r=40, t=60, b=80),
)

# Update Y-axis
fig.update_yaxes(
    title_text=f"<b>{texts.get('y_axis_title', '')}</b>",
    title_font_size=24,
    title_standoff=15,
    showgrid=True,
    gridcolor='#D3D3D3',
    zeroline=True,
    zerolinecolor='black',
    zerolinewidth=1,
    range=[0, 120000],
    dtick=20000,
    tickformat=","
)

# Update X-axis
fig.update_xaxes(
    title_text=texts.get('x_axis_title', ''),
    tickangle=-45,
    showgrid=False,
    showline=False,
)

# Add source/note annotation if present
if caption_text:
    fig.add_annotation(
        text=caption_text,
        xref="paper", yref="paper",
        x=0, y=-0.2, # Adjust position as needed
        showarrow=False,
        align="left",
        xanchor="left",
        yanchor="top",
        font=dict(size=12)
    )

# --- Output ---
output_filename = json_file_path.stem + ".png"
fig.write_image(output_filename, scale=2, width=800, height=600)

print(f"Chart saved to {output_filename}")