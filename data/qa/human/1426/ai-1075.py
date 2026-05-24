import sys
import os
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts from the JSON structure
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
values = [d['value'] for d in chart_data]

# Prepare labels for the pie chart slices, with conditional bolding
pie_texts = []
for i, d in enumerate(chart_data):
    # The "Don't know" label is not bold in the original image
    if "Don't" in d['label']:
         pie_texts.append(f"{d['label']}<br>{d['value']}%")
    else:
        pie_texts.append(f"<b>{d['label']}</b><br>{d['value']}%")

# The smallest slice's label is outside, others are inside
text_positions = ['inside' if item['value'] > 10 else 'outside' for item in chart_data]

# Create the pie chart trace
fig = go.Figure(data=[go.Pie(
    values=values,
    text=pie_texts,
    textinfo='text',
    textposition=text_positions,
    marker_colors=colors,
    sort=False,
    direction='clockwise',
    rotation=90,
    insidetextfont=dict(color='black', size=16),
    outsidetextfont=dict(color='black', size=16),
    hole=0
)])

# Combine title and subtitle
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts.get('subtitle')}"

# Combine source and note for the footer
source_note_text = ""
if texts.get('note'):
    source_note_text += f"<i>{texts.get('note')}</i>"
if texts.get('source'):
    source_note_text += f"<br><b>{texts.get('source')}</b>"


# Update layout for a clean, accurate appearance
fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    title_y=0.95,
    title_font_size=22,
    showlegend=False,
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    margin=dict(l=40, r=40, t=140, b=100),
    annotations=[
        dict(
            text=source_note_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.15,
            align="left",
            xanchor="left",
            yanchor="top",
            font=dict(size=12)
        )
    ]
)

# Determine output filename from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")