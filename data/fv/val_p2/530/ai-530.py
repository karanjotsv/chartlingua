import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the first and only command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data and text from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# --- 2. Prepare Data for Plotly ---
if not chart_data:
    print("Error: 'chart_data' is empty or missing in the JSON file.")
    sys.exit(1)

# Extract categories and values, preserving order
categories = [item['category'] for item in chart_data]
# Assuming a single series of values as per the image
series_data = [item['values'][0] for item in chart_data]

# --- 3. Create the Chart ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=series_data,
    marker_color=colors[0] if colors else '#FF0000',
    showlegend=False
))

# --- 4. Configure Layout and Styling ---
# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='auto',
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 100],
        showgrid=True,
        gridcolor='lightgrey'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=False,
    margin=dict(l=50, r=50, t=90, b=50) # Adjust margins for title and potential source
)

# Combine and add source/note as an annotation
source_note_parts = []
if texts.get('source'):
    source_note_parts.append(texts['source'])
if texts.get('note'):
    source_note_parts.append(texts['note'])
source_note_text = "<br>".join(source_note_parts)

if source_note_text:
    fig.add_annotation(
        text=source_note_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.15,
        xanchor='left',
        yanchor='top'
    )

# --- 5. Output the Chart ---
# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as '{output_filename}'")