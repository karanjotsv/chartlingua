import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data ---
# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Validate and read the JSON file
json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# --- 2. Create Figure ---
fig = go.Figure()

# --- 3. Add Traces ---
# Iterate through the data series in the JSON and add them to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        width=0.9
    ))

# --- 4. Configure Layout ---
# Combine title and subtitle using HTML for better formatting
title_text = ""
if texts.get("title"):
    title_text += f'<span style="font-size: 24px;"><b>{texts["title"]}</b></span>'
if texts.get("subtitle"):
    title_text += f'<br><span style="font-size: 16px;">{texts["subtitle"]}</span>'

fig.update_layout(
    font_family="Arial",
    font_color="black",
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        range=[-0.7, 20.5],
        tickvals=[0, 5, 10, 15, 20],
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        ticks='inside',
        tickwidth=2,
        tickcolor='black',
        ticklen=6,
        showgrid=False,
        minor=dict(
            dtick=1,
            ticklen=4,
            tickwidth=1,
            tickcolor='black',
            showgrid=False
        )
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 0.145],
        dtick=0.02,
        tickformat=',.2f',
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        ticks='inside',
        tickwidth=2,
        tickcolor='black',
        ticklen=6,
        showgrid=False
    ),
    margin=dict(l=60, r=20, t=30, b=40)
)

# --- 5. Add Annotations (Source/Note) ---
# Combine source and note for a single annotation block
source_note_text = ""
if texts.get("source"):
    source_note_text += f'Source: {texts["source"]}'
if texts.get("note"):
    if source_note_text:
        source_note_text += "<br>"
    source_note_text += f'Note: {texts["note"]}'

if source_note_text:
    fig.add_annotation(
        text=source_note_text,
        xref="paper", yref="paper",
        x=0, y=-0.15,
        showarrow=False,
        align="left",
        xanchor='left',
        yanchor='top',
        font=dict(size=12)
    )

# --- 6. Output Image ---
# Derive the output filename from the input JSON path
output_filename = json_file_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")