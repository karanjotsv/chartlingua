import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for the pie chart
labels = [item.get('label', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]
pie_text = [f"{item.get('label', '')}; {item.get('value', 0)}" for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=pie_text,
    textinfo='text',
    textposition='inside',
    insidetextfont=dict(color='black', size=16),
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=1)
    ),
    hole=0,
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    showlegend=False
))

# Build title and subtitle string
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Build source and note string
source_note_text = ""
source = texts.get('source')
note = texts.get('note')
if source:
    source_note_text += f"<i>Source: {source}</i>"
if note:
    if source_note_text:
        source_note_text += f"<br>Note: {note}"
    else:
        source_note_text += f"Note: {note}"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        yanchor='top',
        y=0.95
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(t=80, b=80, l=40, r=40),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Add source/note annotation if it exists
if source_note_text:
    fig.add_annotation(
        text=source_note_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=0,
        xanchor='left',
        yanchor='top',
        yshift=-10  # Shift down from the bottom margin
    )

# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")