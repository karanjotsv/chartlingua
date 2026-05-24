import sys
import json
import plotly.graph_objects as go
import os

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the first and only command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# --- 2. Extract Data and Texts ---
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create the Chart ---
fig = go.Figure()

# Add the pie trace, ensuring data order is preserved
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
    textinfo='percent',
    hoverinfo='label+percent',
    textfont=dict(size=18, family="Arial"),
    sort=False # This is crucial to preserve the order from the JSON file
))

# --- 4. Configure Layout ---
# Combine title and subtitle if both exist
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Combine source and note for an annotation
# Not used for this chart, but the logic is here for robustness
source_note_text = []
if texts.get('source'):
    source_note_text.append(texts['source'])
if texts.get('note'):
    source_note_text.append(texts['note'])
caption_text = "<br>".join(source_note_text)

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    title_font_size=24,
    margin=dict(l=40, r=40, t=120, b=80),
    showlegend=True
)

if caption_text:
    fig.add_annotation(
        text=caption_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.1, # Position below the chart
        xanchor='left',
        yanchor='top'
    )


# --- 5. Output the Image ---
# Derive the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")