import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data for the chart
chart_data = data.get('chart_data', [])
texts = data.get('texts', {})
colors = data.get('colors', {})

labels = [item.get('label', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]
slice_colors = colors.get('slices', [])
text_colors = colors.get('text', [])

# Create the donut chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.45,
    marker_colors=slice_colors,
    texttemplate='%{label}<br>%{value}%',
    textposition='inside',
    insidetextfont={
        'family': 'Arial',
        'size': 24,
        'color': text_colors
    },
    hoverinfo='none',
    sort=False,
    direction='clockwise'
))

# Combine title and subtitle
title_parts = []
if texts.get('title'):
    title_parts.append(f"<span style='font-size: 24px;'><b>{texts['title']}</b></span>")
if texts.get('subtitle'):
    title_parts.append(f"<span style='font-size: 18px;'>{texts['subtitle']}</span>")
final_title = "<br>".join(title_parts)

# Update layout
fig.update_layout(
    title_text=final_title if final_title else None,
    title_x=0.5,
    showlegend=False,
    paper_bgcolor='#000000',
    plot_bgcolor='#000000',
    font_family='Arial',
    margin=dict(l=20, r=20, t=50, b=20)
)

# Combine source and note for an annotation
caption_parts = []
if texts.get('source'):
    caption_parts.append(texts['source'])
if texts.get('note'):
    caption_parts.append(texts['note'])
final_caption = "<br>".join(caption_parts)

if final_caption:
    fig.add_annotation(
        text=final_caption,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.05,
        xanchor='left',
        yanchor='top',
        font={'size': 12, 'family': 'Arial'}
    )

# Determine output filename and save the image
output_filename_base = os.path.splitext(json_path)[0]
output_filename_png = f"{output_filename_base}.png"

fig.write_image(output_filename_png, scale=2)

print(f"Chart saved to {output_filename_png}")