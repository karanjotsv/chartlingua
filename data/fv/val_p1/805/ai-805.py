import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and text from the JSON structure
data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
pull_values = chart_info.get('pull', [])

labels = [d['label'] for d in data]
values = [d['value'] for d in data]

# Prepare custom text for slices to match original layout (line break for large slices)
custom_text = []
for d in data:
    if d['value'] > 20:  # Heuristic based on the original chart's text wrapping
        custom_text.append(f"{d['label']}<br>{d['value']}%")
    else:
        custom_text.append(f"{d['label']} {d['value']}%")

# Create the figure and add the pie chart trace
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=2)),
    pull=pull_values,
    text=custom_text,
    textinfo='text',
    insidetextfont=dict(family="Arial", size=14, color='black'),
    hoverinfo='label+percent',
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise'
))

# Configure the chart's layout, title, and fonts
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

source_text_parts = []
if texts.get('source'):
    source_text_parts.append(texts['source'])
if texts.get('note'):
    source_text_parts.append(texts['note'])
source_text = "<br>".join(source_text_parts)

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=28, color='black')
    ),
    font=dict(family="Arial"),
    showlegend=False,
    margin=dict(t=120, b=80, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Add a source/note annotation if present in the JSON
if source_text:
    fig.add_annotation(
        text=source_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=0,
        yanchor='top',
        xanchor='left',
        font=dict(family="Arial", size=12, color='grey')
    )

# Generate and save the output image
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")